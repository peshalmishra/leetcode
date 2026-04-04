import os

stats = {"easy": 0, "medium": 0, "hard": 0}
recent = []

for k in stats:
    if os.path.exists(k):
        files = [f for f in os.listdir(k) if not f.startswith('.')]
        stats[k] = len(files)
        recent += files

total = sum(stats.values())
recent = sorted(recent, reverse=True)[:5]

recent_lines = "\n".join(f"- `{r}`" for r in recent) if recent else "- No problems yet"

goal = 300
progress_filled = int((total / goal) * 20)
progress_bar = "█" * progress_filled + "░" * (20 - progress_filled)
progress_pct = round((total / goal) * 100, 1)

readme = f"""# 🚀 LeetCode Journey — Peshal Mishra

<div align="center">

[![LeetCode](https://img.shields.io/badge/LeetCode-PeshalMishra-FFA116?style=for-the-badge&logo=leetcode&logoColor=white)](https://leetcode.com/u/PeshalMishra/)
[![BTech CSE](https://img.shields.io/badge/BTech-CSE-0ea5e9?style=for-the-badge)](https://leetcode.com/u/PeshalMishra/)
[![Cloud Architect](https://img.shields.io/badge/Aspiring-Cloud%20Architect-7c3aed?style=for-the-badge&logo=amazonaws&logoColor=white)](https://leetcode.com/u/PeshalMishra/)

</div>

---

## 📊 Stats (auto-updated)

<div align="center">

![Easy](https://img.shields.io/badge/Easy-{stats['easy']}-00b8a3?style=for-the-badge)
![Medium](https://img.shields.io/badge/Medium-{stats['medium']}-ffc01e?style=for-the-badge)
![Hard](https://img.shields.io/badge/Hard-{stats['hard']}-ef4743?style=for-the-badge)
![Total](https://img.shields.io/badge/Total%20Solved-{total}-5b21b6?style=for-the-badge)

</div>

---

## 🎯 Goal Progress

```
{progress_bar} {progress_pct}%
{total} / {goal} problems solved — {goal - total} remaining
```

---

## 🔥 Recent Problems

{recent_lines}

---

## 🛠️ Languages

![C++](https://img.shields.io/badge/C++-00599C?style=flat-square&logo=c%2B%2B&logoColor=white)
![Java](https://img.shields.io/badge/Java-ED8B00?style=flat-square&logo=openjdk&logoColor=white)

---

## 📅 Goals

- ✅ Solve **300+** problems
- ✅ Master **DSA**
- ☁️ Become a **Cloud Architect**

---

<div align="center">
  <sub>Stats auto-updated daily by GitHub Actions · tracked from local solution files</sub>
</div>
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme.strip())

print(f"README updated — Total: {total} | Easy: {stats['easy']} | Medium: {stats['medium']} | Hard: {stats['hard']}")