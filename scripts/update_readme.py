import os

stats = {"easy":0,"medium":0,"hard":0}
recent = []

for k in stats:
    if os.path.exists(k):
        files = os.listdir(k)
        stats[k] = len(files)
        recent += files

total = sum(stats.values())
recent = sorted(recent, reverse=True)[:5]

readme = f"""
# 🚀 LeetCode Journey

## 👨‍💻 About Me
- BTech CSE Student
- Aspiring Cloud Architect ☁️

---

## 📊 Stats
- Total Solved: {total}
- Easy: {stats['easy']} | Medium: {stats['medium']} | Hard: {stats['hard']}

---

## 🔥 Recent Problems
"""

for r in recent:
    readme += f"- {r}\n"

readme += """
---

## 📅 Goal
- 300+ Problems
- Master DSA
"""

with open("README.md", "w", encoding="utf-8") as f:
    f.write(readme)