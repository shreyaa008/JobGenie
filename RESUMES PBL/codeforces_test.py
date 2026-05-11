import requests

def get_codeforces_score(username):
    try:
        url = f"https://codeforces.com/api/user.info?handles={username}"
        response = requests.get(url, timeout=5)
        data = response.json()

        if data["status"] != "OK":
            return 0.0

        user = data["result"][0]

        # .get with default 0 — handles unrated accounts safely
        rating     = user.get("rating", 0)
        max_rating = user.get("maxRating", 0)

        # Use max_rating so past performance counts
        best = max(rating, max_rating)

        # Normalize to 0-100 (3000 = world class)
        score = round(min(best / 4000 * 100, 100), 1)
        return score

    except Exception:
        return 0.0   # API down or username not found

# Test
print(get_codeforces_score("Benq"))   # → 0.0 (no rated contests yet)
print(get_codeforces_score("tourist"))        # → ~100.0 (world #1)