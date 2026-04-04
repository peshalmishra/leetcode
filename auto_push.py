import os
import subprocess
import time

WATCH_DIR = "."

def run(cmd):
    subprocess.run(cmd, shell=True)

def get_files():
    files = []
    for root, _, f in os.walk(WATCH_DIR):
        for file in f:
            if file.endswith(".cpp"):
                files.append(os.path.join(root, file))
    return set(files)

print("Watching for new LeetCode files...")

seen = get_files()

while True:
    time.sleep(5)
    current = get_files()
    new_files = current - seen
    
    if new_files:
        for f in new_files:
            name = os.path.basename(f)
            msg = f"LC {name}"
            
            print(f"New file detected: {name}")
            
            run("git add .")
            run(f'git commit -m "{msg}"')
            run("git push origin main")
            
        seen = current