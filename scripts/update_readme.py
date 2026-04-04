import os
import urllib.request
import json

# --- Fetch live stats from LeetCode API ---
def fetch_leetcode_stats(username):
    try:
        url = f"https://leetcode-stats-api.herokuapp.com/{username}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=10) as res:
            data = json.loads(res.read().decode())
        if data.get("status") == "success":
            return data
    except Exception as e:
        print(f"API fetch failed: {e}")
    return None

USERNAME = "PeshalMishra"
data = fetch_leetcode_stats(USERNAME)

if data:
    easy    = data.get("easySolved", 0)
    medium  = data.get("mediumSolved", 0)
    hard    = data.get("hardSolved", 0)
    total   = data.get("totalSolved", 0)
    ranking = data.get("ranking", "N/A")
    accept  = round(data.get("acceptanceRate", 0), 1)
    source  = "leetcode api"
    print(f"Live stats fetched — Total: {total} | Easy: {easy} | Medium: {medium} | Hard: {hard} | Rank: {ranking}")
else:
    # Fallback: count local files
    stats = {"easy": 0, "medium": 0, "hard": 0}
    for k in stats:
        if os.path.exists(k):
            files = [f for f in os.listdir(k) if not f.startswith('.')]
            stats[k] = len(files)
    easy   = stats["easy"]
    medium = stats["medium"]
    hard   = stats["hard"]
    total  = easy + medium + hard
    ranking = "N/A"
    accept  = "N/A"
    source  = "local files (api unavailable)"
    print(f"Fallback to local count — Total: {total}")

# --- Recent problems from local folders ---
recent = []
for k in ["easy", "medium", "hard"]:
    if os.path.exists(k):
        recent += os.listdir(k)
recent = sorted([f for f in recent if not f.startswith('.')], reverse=True)[:5]
recent_lines = "\n".join(f"- `{r}`" for r in recent) if recent else "- No local solutions yet"

# --- Progress bar ---
goal = 300
progress_filled = min(20, int((total / goal) * 20))
progress_bar = "█" * progress_filled + "░" * (20 - progress_filled)
progress_pct = round(min((total / goal) * 100, 100), 1)

# --- Write README ---
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
{progress_bar}  {progress_pct}%
{total} / {goal} solved · {max(0, goal - total)} remaining
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
  <sub>Stats fetched live from LeetCode · auto-updated daily via GitHub Actions · source: {source}</sub>
</div>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme.strip())

print("README.md written successfully.")