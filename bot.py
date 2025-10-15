import feedparser
import requests
import os

DISCORD_WEBHOOK = os.getenv("DISCORD_WEBHOOK")
RSS_FEED_URL = os.getenv("RSS_FEED_URL")
LAST_TWEET_FILE = "last_tweet.txt"

def get_latest_tweet():
    feed = feedparser.parse(RSS_FEED_URL)
    if not feed.entries:
        return None, None, None
    latest = feed.entries[0]
    link = latest.link
    title = latest.title
    published = latest.published if "published" in latest else ""
    return link, title, published

def already_posted(link):
    if not os.path.exists(LAST_TWEET_FILE):
        return False
    with open(LAST_TWEET_FILE, "r") as f:
        last = f.read().strip()
    return last == link

def save_last_post(link):
    with open(LAST_TWEET_FILE, "w") as f:
        f.write(link)

def post_to_discord(title, link, published):
    embed = {
        "title": "🕊️ EsportsMNG Update",
        "description": f"**New drop from EsportsMNG — don’t miss it 👀**\n\n{title}\n\n[View Tweet]({link})",
        "color": 16753920,
        "footer": {
            "text": f"Posted on {published}",
            "icon_url": "https://raw.githubusercontent.com/pizkodev/daily-tweet-discord-bot/main/mng_scontornato_big.png"
        },
        "thumbnail": {
            "url": "https://raw.githubusercontent.com/pizkodev/daily-tweet-discord-bot/main/mng_scontornato_big.png"
        },
        "image": {
            "url": "https://raw.githubusercontent.com/pizkodev/daily-tweet-discord-bot/main/mngesports.png"
        }
    }

    payload = {
        "username": "MNG Esports Bot",
        "avatar_url": "https://raw.githubusercontent.com/pizkodev/daily-tweet-discord-bot/main/mng_scontornato_big.png",
        "embeds": [embed]
    }

    response = requests.post(DISCORD_WEBHOOK, json=payload)
    if response.status_code == 204:
        print("✅ Messaggio inviato con successo su Discord.")
    else:
        print(f"⚠️ Errore invio messaggio: {response.status_code} - {response.text}")

if __name__ == "__main__":
    link, title, published = get_latest_tweet()
    if link and not already_posted(link):
        post_to_discord(title, link, published)
        save_last_post(link)
    else:
        print("Nessun nuovo tweet trovato.")
