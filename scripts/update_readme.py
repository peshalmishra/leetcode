import os
import json
import ssl
import certifi
import urllib.request
import urllib.error

USERNAME = "PeshalMishra"

GRAPHQL_URL = "https://leetcode.com/graphql"

HEADERS = {
    "Content-Type": "application/json",
    "User-Agent": "Mozilla/5.0",
    "Referer": "https://leetcode.com",
    "Origin": "https://leetcode.com",
}

# ✅ Fix SSL globally
SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())


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


# -------------------------------
# 🔹 API HELPERS
# -------------------------------

def fetch_json(url, data=None):
    try:
        req = urllib.request.Request(url, data=data, headers=HEADERS)
        with urllib.request.urlopen(req, context=SSL_CONTEXT, timeout=15) as res:
            return json.loads(res.read().decode())
    except Exception as e:
        print(f"❌ API Error ({url}): {e}")
        return None


def fetch_graphql():
    payload = json.dumps({
        "query": QUERY,
        "variables": {"username": USERNAME}
    }).encode("utf-8")

    return fetch_json(GRAPHQL_URL, payload)


def parse_graphql(data):
    try:
        user = data["data"]["matchedUser"]
        ranking = user["profile"]["ranking"]

        counts = {
            item["difficulty"]: item["count"]
            for item in user["submitStats"]["acSubmissionNum"]
        }

        return {
            "total": counts.get("All", 0),
            "easy": counts.get("Easy", 0),
            "medium": counts.get("Medium", 0),
            "hard": counts.get("Hard", 0),
            "ranking": ranking,
        }
    except Exception:
        return None


def fetch_rest():
    urls = [
        f"https://alfa-leetcode-api.onrender.com/{USERNAME}/solved",
        f"https://leetcode-stats.tashif.codes/{USERNAME}",
    ]

    for url in urls:
        print(f"🌐 Trying REST: {url}")
        data = fetch_json(url)

        if not data or data.get("errors"):
            continue

        return {
            "easy": data.get("easySolved", 0),
            "medium": data.get("mediumSolved", 0),
            "hard": data.get("hardSolved", 0),
            "total": data.get("solvedProblem", data.get("totalSolved", 0)),
            "ranking": data.get("ranking", "N/A"),
        }

    return None


def fetch_local():
    print("📂 Using local file fallback")

    counts = {}
    for level in ["easy", "medium", "hard"]:
        if os.path.exists(level):
            counts[level] = len([
                f for f in os.listdir(level)
                if not f.startswith(".")
            ])
        else:
            counts[level] = 0

    return {
        "easy": counts["easy"],
        "medium": counts["medium"],
        "hard": counts["hard"],
        "total": sum(counts.values()),
        "ranking": "N/A",
    }


# -------------------------------
# 🔹 MAIN DATA FETCH
# -------------------------------

def get_stats():
    print("🔍 Fetching LeetCode stats...")

    # GraphQL
    data = fetch_graphql()
    stats = parse_graphql(data) if data else None

    if stats:
        print("✅ GraphQL success")
        return stats, "leetcode graphql"

    # REST fallback
    stats = fetch_rest()
    if stats:
        print("✅ REST success")
        return stats, "rest api"

    # Local fallback
    return fetch_local(), "local files"


# -------------------------------
# 🔹 README GENERATION
# -------------------------------

def get_recent():
    files = []
    for level in ["easy", "medium", "hard"]:
        if os.path.exists(level):
            files += [
                f for f in os.listdir(level)
                if not f.startswith(".")
            ]

    files = sorted(files, reverse=True)[:5]
    return "\n".join(f"- `{f}`" for f in files) or "- No solutions yet"


def progress_bar(total, goal=300):
    filled = min(20, int((total / goal) * 20))
    bar = "█" * filled + "░" * (20 - filled)
    pct = round(min((total / goal) * 100, 100), 1)
    remaining = max(0, goal - total)

    return bar, pct, remaining


def generate_readme(stats, source):
    easy = stats["easy"]
    medium = stats["medium"]
    hard = stats["hard"]
    total = stats["total"]
    ranking = stats["ranking"]

    bar, pct, remaining = progress_bar(total)
    recent = get_recent()

    return f"""# 🚀 LeetCode Journey — Peshal Mishra

## 📊 Stats
- Easy: {easy}
- Medium: {medium}
- Hard: {hard}
- Total: {total}
- Rank: {ranking}

## 🎯 Progress (300 Goal)

## 🔥 Recent Solutions
{recent}

---
Auto-updated · {source}
"""


# -------------------------------
# 🔹 RUN
# -------------------------------

def main():
    stats, source = get_stats()

    readme = generate_readme(stats, source)

    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme.strip())

    print("✅ README.md updated successfully")


if __name__ == "__main__":
    main()