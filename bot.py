import feedparser
import requests
import os

# Variabili d’ambiente (dal repo GitHub → Settings → Secrets)
DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
RSS_FEED_URL = os.getenv("RSS_FEED_URL")
LAST_TWEET_FILE = "last_tweet.txt"

def get_latest_tweet():
    feed = feedparser.parse(RSS_FEED_URL)
    if not feed.entries:
        return None, None
    latest = feed.entries[0]
    return latest.link, latest.title

def already_posted(link):
    if not os.path.exists(LAST_TWEET_FILE):
        return False
    with open(LAST_TWEET_FILE, "r") as f:
        last = f.read().strip()
    return last == link

def save_last_post(link):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(link)

def post_to_discord(title, link):
    data = {
        "content": f"🕊️ **New Tweet Posted!**\n**{title}**\n{link}"
    }
    requests.post(DISCORD_WEBHOOK, json=data)

if __name__ == "__main__":
    link, title = get_latest_tweet()
    if link and not already_posted(link):
        post_to_discord(title, link)
        save_last_post(link)
    else:
        print("Nessun nuovo tweet trovato.")
