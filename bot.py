import requests
import os
import tweepy

# Parametri da GitHub Secrets
BEARER_TOKEN = os.environ.get("BEARER_TOKEN")
TWITTER_USERNAME = os.environ.get("TWITTER_USERNAME")
DISCORD_WEBHOOK = os.environ.get("DISCORD_WEBHOOK")

# Controllo variabili
if not BEARER_TOKEN or not TWITTER_USERNAME or not DISCORD_WEBHOOK:
    raise ValueError("Assicurati che BEARER_TOKEN, TWITTER_USERNAME e DISCORD_WEBHOOK siano impostati nelle variabili d'ambiente!")

# Configura Tweepy client v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Prendi l'ultimo tweet dell'utente
user = client.get_user(username=TWITTER_USERNAME)
tweets = client.get_users_tweets(user.data.id, max_results=5, tweet_fields=["created_at","text","id"])

if tweets.data:
    latest = tweets.data[0]
    tweet_text = latest.text
    tweet_url = f"https://x.com/{TWITTER_USERNAME}/status/{latest.id}"

    # Invia su Discord
    data = {
        "content": f"{tweet_text}\n{tweet_url}"
    }
    response = requests.post(DISCORD_WEBHOOK, json=data)
    if response.status_code == 204:
        print("Posted successfully to Discord!")
    else:
        print(f"Error posting to Discord: {response.status_code} - {response.text}")
else:
    print("No tweets found.")
