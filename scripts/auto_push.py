import subprocess

BRANCH = "main"
REMOTE = "origin"
COMMIT_MSG = "auto update"


def run(cmd):
    """Run command and print output"""
    result = subprocess.run(cmd, shell=True, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout.strip())
    if result.stderr:
        print(result.stderr.strip())

    return result


def has_changes():
    """Check if repo has changes"""
    result = run("git status --porcelain")
    return result.stdout.strip() != ""


def pull_latest():
    """Pull latest changes with rebase"""
    print("⬇️ Pulling latest changes...")
    result = run(f"git pull {REMOTE} {BRANCH} --rebase")

    if result.returncode != 0:
        print("⚠️ Conflict detected. Resolving README...")
        run("git checkout --ours README.md")
        run("git add README.md")
        run("git rebase --continue")


def commit_changes():
    """Commit changes if any"""
    run("git add .")
    result = run(f'git commit -m "{COMMIT_MSG}"')

    if result.returncode != 0:
        print("⚠️ Nothing to commit")
        return False

    print("✅ Commit created")
    return True


def push_changes():
    """Push changes with retry"""
    print("⬆️ Pushing changes...")
    result = run(f"git push {REMOTE} {BRANCH}")

    if result.returncode != 0:
        print("⚠️ Push failed. Retrying...")
        pull_latest()
        run(f"git push {REMOTE} {BRANCH}")


def main():
    print("🚀 Running auto push...")

    # Step 1: pull first
    pull_latest()

    # Step 2: commit if changes exist
    if has_changes():
        if commit_changes():
            push_changes()
    else:
        print("✅ No changes found")

    print("🎉 Done!")


if __name__ == "__main__":
    main()