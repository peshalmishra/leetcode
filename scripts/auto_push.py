import os
import subprocess
import time
import shutil

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

def detect_topic(name):
    name = name.lower()
    
    if any(k in name for k in ["dp", "square", "coin", "subset"]):
        return "dp"
    if any(k in name for k in ["graph", "bfs", "dfs"]):
        return "graphs"
    if any(k in name for k in ["tree", "bst"]):
        return "trees"
    if any(k in name for k in ["array", "sum"]):
        return "arrays"
    if any(k in name for k in ["string", "palindrome"]):
        return "strings"
    
    return None

print("Watching for new files...")

seen = get_files()

while True:
    time.sleep(5)
    current = get_files()
    new_files = current - seen
    
    if new_files:
        for f in new_files:
            name = os.path.basename(f)
            topic = detect_topic(name)
            
            if topic:
                dest_dir = os.path.join("topics", topic)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy(f, os.path.join(dest_dir, name))
                print(f"Copied to topics/{topic}/")
            
            msg = f"LC {name}"
            
            run("git add .")
            run(f'git commit -m "{msg}"')
            run("git push origin main")
        
        seen = current