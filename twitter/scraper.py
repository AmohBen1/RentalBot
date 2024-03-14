from datetime import datetime
import re

###### TWITTER PARSING #######
# A function to match different date formats
def match_date(text):
    # List of different date regex patterns to match
    date_patterns = [
        r'\b(\d{1,2}/\d{1,2}/\d{4})\b',  # Matches dates like 2/15/2024
        r'\b(\w+ \d{1,2}(?:st|nd|rd|th)?, \d{4})\b',  # Matches dates like February 15th, 2024
        r'\b(\w+. \d{1,2} \d{4})\b'  # Matches dates like Feb. 15 2024
    ]
    for pattern in date_patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
    return None

# Function to parse a tweet into a listing dictionary
def parse_tweet(tweet_text):
    # Regex patterns to match various parts of the listing
    graduate_students_pattern = re.compile(r'graduate students', re.IGNORECASE)
    bedrooms_pattern = re.compile(r'(\d+) ?(bedrooms?|beds?)', re.IGNORECASE)
    bathrooms_pattern = re.compile(r'(\d+) ?(bathrooms?|baths?)', re.IGNORECASE)
    price_pattern = re.compile(r'\$(\d+)')

    # Search for the patterns in the tweet text
    grad_students_match = graduate_students_pattern.search(tweet_text)
    bedrooms_match = bedrooms_pattern.search(tweet_text)
    bathrooms_match = bathrooms_pattern.search(tweet_text)
    price_match = price_pattern.search(tweet_text)
    date_match = match_date(tweet_text)

    # Extract the matching text if found
    graduate_students = 'yes' if grad_students_match else 'no'
    bedrooms = bedrooms_match.group(1) if bedrooms_match else 'N/A'
    bathrooms = bathrooms_match.group(1) if bathrooms_match else 'N/A'
    price = int(price_match.group(1)) if price_match else 'N/A'
    # Try to parse the date, if matched
    if date_match:
        try:
            available_date = datetime.strptime(date_match, '%m/%d/%Y')
        except ValueError:
            try:
                available_date = datetime.strptime(date_match, '%B %d%Y')
            except ValueError:
                try:
                    available_date = datetime.strptime(date_match, '%b %d %Y')
                except ValueError:
                    available_date = 'N/A'
    else:
        available_date = 'N/A'

    return {
        'graduate_students': graduate_students,
        'bedrooms': bedrooms,
        'bathrooms': bathrooms,
        'price': price,
        'available_date': available_date
    }

def extract_url_from_tweet(tweet_text):
    # Use regular expression to match URLS 
    url_pattern = r'https?://[^\s]+'