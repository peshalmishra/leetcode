import os
import urllib.request
import urllib.error
import json

def fetch(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        print(f"  failed: {e}")
        return None

USERNAME = "PeshalMishra"
data = None

# Try multiple APIs in order
apis = [
    f"https://alfa-leetcode-api.onrender.com/{USERNAME}/solved",
    f"https://leetcode-stats.tashif.codes/{USERNAME}",
    f"https://leetcode-stats-api.herokuapp.com/{USERNAME}",
]

print("Trying LeetCode APIs...")
for url in apis:
    print(f"  -> {url}")
    result = fetch(url)
    if result and not result.get("errors"):
        data = result
        print(f"  OK: {url}")
        break

if data:
    # alfa-leetcode-api returns solvedProblem / easySolved etc
    easy   = data.get("easySolved",   data.get("easySolved",   0))
    medium = data.get("mediumSolved", data.get("mediumSolved", 0))
    hard   = data.get("hardSolved",   data.get("hardSolved",   0))
    total  = data.get("solvedProblem",data.get("totalSolved",  easy + medium + hard))
    ranking= data.get("ranking", "N/A")
    accept = data.get("acceptanceRate", "N/A")
    if isinstance(accept, float):
        accept = round(accept, 1)
    source = "leetcode api (live)"
    print(f"Stats: Total={total} Easy={easy} Med={medium} Hard={hard}")
else:
    # Fallback: count local solution files
    print("All APIs failed, falling back to local file count.")
    counts = {}
    for k in ["easy", "medium", "hard"]:
        if os.path.exists(k):
            counts[k] = len([f for f in os.listdir(k) if not f.startswith('.')])
        else:
            counts[k] = 0
    easy, medium, hard = counts["easy"], counts["medium"], counts["hard"]
    total   = easy + medium + hard
    ranking = "N/A"
    accept  = "N/A"
    source  = "local files (all apis down)"

# Recent solutions from local folders
recent = []
for k in ["easy", "medium", "hard"]:
    if os.path.exists(k):
        recent += [f for f in os.listdir(k) if not f.startswith('.')]
recent = sorted(recent, reverse=True)[:5]
recent_lines = "\n".join(f"- `{r}`" for r in recent) if recent else "- No local solutions yet"

# Progress bar toward goal
goal = 300
filled = min(20, int((total / goal) * 20))
bar = "█" * filled + "░" * (20 - filled)
pct = round(min((total / goal) * 100, 100), 1)
remaining = max(0, goal - total)

readme = f"""# 🚀 LeetCode Journey — Peshal Mishra

<div align="center">

[![LeetCode](https://img.shields.io/badge/LeetCode-PeshalMishra-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/u/PeshalMishra/)
[![LPU](https://img.shields.io/badge/LPU-BTech%20CSE-0ea5e9?style=for-the-badge)](https://leetcode.com/u/PeshalMishra/)
[![Cloud](https://img.shields.io/badge/Aspiring-Cloud%20Architect-7c3aed?style=for-the-badge&logo=amazonaws&logoColor=white)](https://leetcode.com/u/PeshalMishra/)

</div>

---

## 📊 Live Stats

<div align="center">

![Easy](https://img.shields.io/badge/Easy-{easy}-00b8a3?style=for-the-badge)
![Medium](https://img.shields.io/badge/Medium-{medium}-ffc01e?style=for-the-badge)
![Hard](https://img.shields.io/badge/Hard-{hard}-ef4743?style=for-the-badge)
![Total](https://img.shields.io/badge/Total%20Solved-{total}-5b21b6?style=for-the-badge)
![Rank](https://img.shields.io/badge/Global%20Rank-{ranking}-0ea5e9?style=for-the-badge)
![Acceptance](https://img.shields.io/badge/Acceptance-{accept}%25-16a34a?style=for-the-badge)

</div>

---

## 🎯 Goal Progress — 300 Problems

```
{bar}  {pct}%
{total} / {goal} solved · {remaining} remaining
```

---

## 🔥 Recent Solutions

{recent_lines}

---

## 🛠️ Languages

![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)
![Python](https://img.shields.io/badge/Python-3776AB?style=flat-square&logo=python&logoColor=white)

---

## 📅 Goals

- ✅ Solve **300+** problems
- ✅ Master **DSA**
- ☁️ Become a **Cloud Architect**

---

<div align="center">
  <sub>Auto-updated daily via GitHub Actions · {source}</sub>
</div>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme.strip())

print("README.md written successfully.")