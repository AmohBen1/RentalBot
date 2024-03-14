from website.scraper import get_listings
from website.form_filler import fill_form_with_details
from utils import send_notification
from datetime import datetime
from website.scraper import *

def run_bot():
    # Step 1: Scrape new listings
    listings = get_listings()

    # Filter listings according to specific criteria not already filtered
    filtered_listings = [listing for listing in listings if meets_criteria(listing)]

    if filtered_listings:
        for listing in filtered_listings:
            # Step 2: Fill and submit the form for each listing
            if fill_form_with_details(listing):
                message = f"Successfully submitted listing: {listing['title']}"
                print(message)
                send_notification("Listing Submission Success", message)
            else:
                send_notification("Listing Submission Failure", f"Failed to submit listing: {listing['title']}")

    else:
        print("No new suitable listings found.")

def meets_criteria(listing):
    # Extract bedroom and bathroom counts and price
    bedrooms = listing.get('bedrooms', '')
    bathrooms = listing.get('bathrooms', '')
    rent_price = listing.get('rent_price', '')
    lease_start_date_st = listing.get('least_start', '')

     # Parse lease start date and compare
    try:
        lease_start_date = datetime.strptime(lease_start_date_st, '%m/%d/%Y')
        cutoff_date = datetime(2024, 5, 1)
        if lease_start_date < cutoff_date:
            return False  # Lease starts before the cutoff date
    except ValueError:
        return False  # Date format is incorrect or lease_start_str is empty

    if (bedrooms == '2' or bedrooms == '2 1/2') and bathrooms ==  '1' and rent_price <= 2000:
        return True
    else:
        return False
    
def meets_twitter_criteria(listing):
    # Assume 'listing' is a dictionary with keys like 'bedrooms', 'bathrooms', 'price', 'graduate_students', etc.
    # Assume 'extract_price' and 'extract_number' are utility functions you've written to parse those values
    bedrooms = extract_number(listing['bedrooms'])
    bathrooms = extract_number(listing['bathrooms'])
    price = extract_price(listing['price'])
    lease_start = datetime.strptime(listing['available_date'], '%m/%d/%Y')

    # Your criteria: 2 bedrooms, 1 bathroom, price less than $2000, lease start after May 1st, 2024
    return ((bedrooms == '2'or bedrooms == '2 1/2') and bathrooms == '1' and 
            price < 2000 and lease_start > datetime(2024, 5, 1))

if __name__ == "__main__":
    run_bot()
