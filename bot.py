import requests
import os
import tweepy

# Parametri da GitHub Secrets
BEARER_TOKEN = os.environ["AAAAAAAAAAAAAAAAAAAAAP544gEAAAAAd2VQEl2Z%2BTf2X3j6m7FZIlcpo5A%3DAA84YbfMwpNY4b8JjXHh5BAVVOZI86ot9O1ydabZYIameP143k"]
TWITTER_USERNAME = os.environ["EsportsMNG"]
DISCORD_WEBHOOK = os.environ["https://discord.com/api/webhooks/1424519710967337053/hEFtwUjAjpqOJV523faPhkVZuTfzdHPg_nR5txjkwyiNC95UMZPtaA3Kn4SrkUq3RJOn"]

# Configura Tweepy client v2
client = tweepy.Client(bearer_token=BEARER_TOKEN)

# Prendi l'ultimo tweet dell'utente
user = client.get_user(username=TWITTER_USERNAME)
tweets = client.get_users_tweets(user.data.id, max_results=5, tweet_fields=["created_at","text","id"])

if tweets.data:
    latest = tweets.data[0]
    tweet_text = latest.text
    tweet_url = f"https://twitter.com/{TWITTER_USERNAME}/status/{latest.id}"

    # Invia su Discord
    data = {
        "content": f"{tweet_text}\n{tweet_url}"
    }
    response = requests.post(DISCORD_WEBHOOK, json=data)
    if response.status_code == 204:
        print("Posted successfully to Discord!")
    else:
        print(f"Error posting to Discord: {response.status_code}")
else:
    print("No tweets found.")
