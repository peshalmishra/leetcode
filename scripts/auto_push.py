import os
import time
import subprocess

def run(cmd):
    return subprocess.run(cmd, shell=True)

def has_changes():
    result = subprocess.run("git status --porcelain", shell=True, capture_output=True, text=True)
    return result.stdout.strip() != ""

while True:
    if has_changes():
        run("git add .")
        run('git commit -m "auto update"')
        pull = subprocess.run("git pull origin main --rebase", shell=True)
        if pull.returncode != 0:
            run("git rebase --abort")
            time.sleep(5)
            continue
        push = subprocess.run("git push origin main", shell=True)
        if push.returncode != 0:
            run("git pull origin main --rebase")
            run("git push origin main")
    time.sleep(10)