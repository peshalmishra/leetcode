import os
import json
import urllib.request
import urllib.error

USERNAME = "PeshalMishra"

GRAPHQL_URL = "https://leetcode.com/graphql"

QUERY = """
query getUserProfile($username: String!) {
  matchedUser(username: $username) {
    profile {
      ranking
    }
    submitStats {
      acSubmissionNum {
        difficulty
        count
      }
    }
  }
}
"""

def fetch_graphql():
    payload = json.dumps({
        "query": QUERY,
        "variables": {"username": USERNAME}
    }).encode("utf-8")

    req = urllib.request.Request(
        GRAPHQL_URL,
        data=payload,
        headers={
            "Content-Type": "application/json",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Referer": "https://leetcode.com",
            "Origin": "https://leetcode.com",
        },
        method="POST"
    )

    with urllib.request.urlopen(req, timeout=15) as res:
        return json.loads(res.read().decode())

def parse_graphql(data):
    user = data["data"]["matchedUser"]
    ranking = user["profile"]["ranking"]
    counts = {item["difficulty"]: item["count"] for item in user["submitStats"]["acSubmissionNum"]}
    return {
        "total":   counts.get("All", 0),
        "easy":    counts.get("Easy", 0),
        "medium":  counts.get("Medium", 0),
        "hard":    counts.get("Hard", 0),
        "ranking": ranking,
    }

# --- Try GraphQL first ---
stats = None
source = ""

print("Trying LeetCode GraphQL API...")
try:
    raw = fetch_graphql()
    stats = parse_graphql(raw)
    source = "leetcode graphql (live)"
    print(f"GraphQL OK — Total: {stats['total']} Easy: {stats['easy']} Med: {stats['medium']} Hard: {stats['hard']} Rank: {stats['ranking']}")
except Exception as e:
    print(f"GraphQL failed: {e}")

# --- Fallback REST APIs ---
if not stats:
    rest_apis = [
        f"https://alfa-leetcode-api.onrender.com/{USERNAME}/solved",
        f"https://leetcode-stats.tashif.codes/{USERNAME}",
    ]
    for url in rest_apis:
        print(f"Trying REST: {url}")
        try:
            req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
            with urllib.request.urlopen(req, timeout=10) as res:
                d = json.loads(res.read().decode())
            if d and not d.get("errors"):
                stats = {
                    "easy":    d.get("easySolved", 0),
                    "medium":  d.get("mediumSolved", 0),
                    "hard":    d.get("hardSolved", 0),
                    "total":   d.get("solvedProblem", d.get("totalSolved", 0)),
                    "ranking": d.get("ranking", "N/A"),
                }
                source = f"rest api: {url}"
                print(f"REST OK — {stats}")
                break
        except Exception as e:
            print(f"  failed: {e}")

# --- Final fallback: local file count ---
if not stats:
    print("All APIs failed. Counting local files.")
    counts = {}
    for k in ["easy", "medium", "hard"]:
        counts[k] = len([f for f in os.listdir(k) if not f.startswith('.')]) if os.path.exists(k) else 0
    stats = {
        "easy": counts["easy"], "medium": counts["medium"], "hard": counts["hard"],
        "total": sum(counts.values()), "ranking": "N/A"
    }
    source = "local files (all apis down)"

easy    = stats["easy"]
medium  = stats["medium"]
hard    = stats["hard"]
total   = stats["total"]
ranking = stats["ranking"]

# --- Recent solutions from local folders ---
recent = []
for k in ["easy", "medium", "hard"]:
    if os.path.exists(k):
        recent += [f for f in os.listdir(k) if not f.startswith('.')]
recent = sorted(recent, reverse=True)[:5]
recent_lines = "\n".join(f"- `{r}`" for r in recent) if recent else "- No local solutions yet"

# --- Progress bar ---
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