import requests
import json
import os
import time
from datetime import datetime

# API URLs
TOP_URL = "https://hacker-news.firebaseio.com/v0/topstories.json"
ITEM_URL = "https://hacker-news.firebaseio.com/v0/item/{}.json"

# Header
HEADERS = {"User-Agent": "TrendPulse/1.0"}

# Updated keywords (improved matching)
CATEGORIES = {
    "technology": ["ai","software","tech","code","computer","data","cloud","api","gpu","llm","startup","app","programming"],
    
    "worldnews": ["war","government","country","president","election","climate","attack","global","india","china","usa","policy","news"],
    
    "sports": ["nfl","nba","fifa","sport","game","team","player","league","championship","match","cricket","football","tournament"],
    
    "science": ["research","study","space","physics","biology","discovery","nasa","genome","experiment","scientists","earth","medicine"],
    
    "entertainment": ["movie","film","music","netflix","game","book","show","award","streaming","series","tv","celebrity"]
}

# Fetch top 500 story IDs
def get_top_ids():
    try:
        res = requests.get(TOP_URL, headers=HEADERS)
        return res.json()[:500]
    except:
        print("Error fetching top stories")
        return []

# Fetch individual story
def get_story(story_id):
    try:
        res = requests.get(ITEM_URL.format(story_id), headers=HEADERS)
        return res.json()
    except:
        print("Error fetching story:", story_id)
        return None

# Check if title matches category keywords
def matches_category(title, keywords):
    title = title.lower()
    for word in keywords:
        if word in title:
            return True
    return False

def main():
    story_ids = get_top_ids()
    collected_data = []

    # Loop through each category separately
    for category, keywords in CATEGORIES.items():
        count = 0
        print(f"\nCollecting {category} stories...")

        for sid in story_ids:
            if count >= 25:
                break

            story = get_story(sid)
            if not story or "title" not in story:
                continue

            # Match category
            if not matches_category(story["title"], keywords):
                continue

            # Extract required fields
            item = {
                "post_id": story.get("id"),
                "title": story.get("title"),
                "category": category,
                "score": story.get("score", 0),
                "num_comments": story.get("descendants", 0),
                "author": story.get("by"),
                "collected_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }

            collected_data.append(item)
            count += 1

        print(f"{category}: {count} stories collected")

        # Required delay after each category
        time.sleep(2)

    # Create folder if not exists
    if not os.path.exists("data"):
        os.makedirs("data")

    # File name with date
    filename = "data/trends_" + datetime.now().strftime("%Y%m%d") + ".json"

    # Save to JSON
    with open(filename, "w") as f:
        json.dump(collected_data, f, indent=4)

    print(f"\nCollected {len(collected_data)} stories. Saved to {filename}")

# Run program
if __name__ == "__main__":
    main()