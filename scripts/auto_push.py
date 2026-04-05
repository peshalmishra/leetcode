import time
import subprocess

BRANCH = "main"
REMOTE = "origin"
COMMIT_MSG = "auto update"
SLEEP_INTERVAL = 10


def run(cmd):
    """Run a shell command and return result"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())
    return result


def has_changes():
    """Check if there are git changes"""
    result = run("git status --porcelain")
    return result.stdout.strip() != ""


def resolve_conflicts():
    """Auto-resolve README.md conflicts by keeping local version"""
    print("⚠️ Conflict detected. Resolving...")

    run("git checkout --ours README.md")
    run("git add README.md")

    cont = run("git rebase --continue")

    # If multiple conflicts, keep resolving
    while cont.returncode != 0:
        print("🔁 Continuing conflict resolution...")
        run("git checkout --ours README.md")
        run("git add README.md")
        cont = run("git rebase --continue")

    print("✅ Conflicts resolved")


def pull_latest():
    """Pull latest changes with rebase"""
    print("⬇️ Pulling latest changes...")
    result = run(f"git pull {REMOTE} {BRANCH} --rebase")

    if result.returncode != 0:
        resolve_conflicts()


def commit_changes():
    """Stage and commit changes"""
    run("git add .")
    result = run(f'git commit -m "{COMMIT_MSG}"')
    return result.returncode == 0


def push_changes():
    """Push changes with retry logic"""
    print("⬆️ Pushing changes...")
    result = run(f"git push {REMOTE} {BRANCH}")

    if result.returncode != 0:
        print("⚠️ Push failed. Retrying after pull...")
        pull_latest()
        run(f"git push {REMOTE} {BRANCH}")


def main():
    print("🚀 Auto push script started...")

    while True:
        try:
            # Step 1: Always sync first
            pull_latest()

            # Step 2: Check changes
            if has_changes():
                print("📝 Changes detected")

                if commit_changes():
                    push_changes()
                else:
                    print("⚠️ Nothing to commit")

            else:
                print("✅ No changes")

        except Exception as e:
            print(f"❌ Error: {e}")

        time.sleep(SLEEP_INTERVAL)


if __name__ == "__main__":
    main()