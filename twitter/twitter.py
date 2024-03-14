import os
import tweepy
from scraper import *
from website.form_filler import *
from form_filler import *
from main import *

consumer_key = os.getenv('TWITTER_CONSUMER_KEY')
consumer_secret = os.getenv('TWITTER_CONSUMER_SECRET')
access_token = os.getenv('TWITTER_ACCESS_TOKEN')
access_token_secret = os.getenv('TWITTER_ACCESS_TOKEN_SECRET')
bearer_token = os.getenv('TWITTER_BEARER_TOKEN')

auth = tweepy.OAuth1UserHandler(
    consumer_key, consumer_secret,
    access_token, access_token_secret
)
api = tweepy.API(auth)

Dartmouth_handle = "DartmouthRE"

# Set up the stream listener
class MyStreamListener(tweepy.StreamingClient):
    def on_tweet(self, tweet):
        print(tweet.text)
        tweet_text = tweet.text
        # Logic to decide whether to scrape the listing
        # Perhaps the tweet contains a URL or some indicator of a new listing
        parsed_tweet = parsed_tweet(tweet_text)
        if meets_criteria(parsed_tweet):
            fill_form_with_details(listing)
            send_notification("Filled form for listing: " + listing['title'])

# Create a streaming client
stream_listener = MyStreamListener(bearer_token=bearer_token)

# Add a rule to the stream for tweets from a specific user (optional, do it once)
# rule = tweepy.StreamRule(f"from:{Dartmouth_handle}")
# stream_listener.add_rules(rule, dry_run=False)

# Start the stream
stream_listener.filter()

# Example usage
stream_listener = MyStreamListener(bearer_token='YOUR_BEARER_TOKEN')
stream_listener.add_rules(tweepy.StreamRule(f"from:{Dartmouth_handle}"))
stream_listener.filter()

tweet_text = "Check out our new listing at Sachem Village! Graduate students preferred. 2 bedroom 1 bathhouse for $1600. Apply now at https://realestate.dartmouth.edu/dartmouth-rentals"

# Extract URL
form_url = extract_url_from_tweet(tweet_text)


# Test credentials and form details
username = "benjamin.k.amoh.th@dartmouth.edu"
password = "Elyon@jehowa0"
form_details = {
    'field_value': 'Some value',  # Example: You'll replace this with actual data you want to submit
}

# Initialize WebDriver
driver = get_driver()

# Log into the site if necessary
login_to_site(driver, username, password, form_url, "username_field_id", "password_field_id", "submit_button_id")

# Fill out and submit the form
fill_form_with_details(driver, form_details, form_url)

