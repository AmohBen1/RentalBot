from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service as ChromeService
# from selenium.webdriver.chrome.options import Options
import re
from bs4 import BeautifulSoup
import time
from datetime import datetime

# WebDriver path setup
DRIVER_PATH = '/Users/mac/Bot/chromedriver-mac-x64/chromedriver'

def get_driver():
    # options = Options()
    # options.headless = True
    # service = Service(executable_path= DRIVER_PATH)
    # return webdriver.Chrome(service=Service, options=options)

    #options = webdriver.ChromeOptions()
    #options.add_argument('headless')  # Runs Chrome in headless mode.
    #return webdriver.Chrome(executable_path=DRIVER_PATH, options=options)

    service = ChromeService(executable_path='/Users/mac/Bot/chromedriver-mac-x64/chromedriver')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Uncomment if you want to run Chrome in headless mode
    driver = webdriver.Chrome(service=service, options=options)
    return driver

def search_listings(driver):
    driver.get("https://realestate.dartmouth.edu/upper-valley-rentals")
    # Wait for the page to load
    time.sleep(2)  # Adjust timing based on page load speed

    # Click on the Dartmouth Graduate Student button
    # grad_student_button = WebDriverWait(driver, 10).until(
    #     EC.element_to_be_clickable((By.ID, 'edit-field-offered-to-value-1')))
    # grad_student_button.click()

    # Click on the Search button
    search_button = driver.find_element(By.ID, "edit-submit-upper-valley-rentals")
    search_button.click()

    # Wait for search results to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'form-submit')))

def extract_number(text):
    """
    Extracts the number from text using regex. Handles whole and fractional numbers.
    Returns the extracted number as a string.
    """
    match = re.search(r'(\d+(?:\.\d+)?)', text)
    return match.group(1) if match else None

def extract_price(text):
    # Remove the dollar sign and commas then convert to float
    return float(re.sub(r'[^\d.]', '', text))

def parse_listings(driver):
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    listings = soup.find_all('div', class_='reo-listing__content')  # Adjust based on actual class for listings

    for listing in listings:
        #Extract details from the listing here
        lease_start_label = listing.find('h4', class_= 'label', string="Lease Start Date:")
        if lease_start_label:
            lease_start_div = lease_start_label.find_next('div', class_='value')
            lease_start_date = lease_start_div.get_text(strip = True)

        #lease_start = listing.find('div', class_= 'field-name-field-reo-uv-from').text.strip()
        # bedroom_label = listing.find('h4', class_= 'label', string="Number of Bedrooms:")
        # if bedroom_label:
        #     bedroom_div = bedroom_label.find_next('div', class_='value')
        #     bedrooms = extract_number(bedroom_div.get_text(strip = True))
        
        bedroom_div = listing.find('div', class_='field-name-field-reo-num-bedrooms')
        if bedroom_div:
            bedroom_value = bedroom_div.find('div', class_='value')
            if bedroom_value:
                bedrooms = extract_number(bedroom_value.get_text(strip = True))
            else: 
                bedrooms = 'N/A'
        else: 
            bedrooms = 'N/A'

        # bathroom_label = listing.find('h4', class_= 'label', string="Number of Bathrooms:")
        bathroom_div = listing.find('div', class_='field-name-field-reo-num-bathrooms')
        if bathroom_div:
            bathroom_value = bathroom_div.find('div', class_='value')
            if bathroom_value:
                bathrooms = extract_number(bathroom_value.get_text(strip = True))
            else: 
                bathrooms = 'N/A'
        else: 
            bathrooms = 'N/A'

        
        #bedrooms = listing.find('div', class_= 'field-name-field-reo-num-bedrooms').text.strip()
        #bathrooms = listing.find('div', class_='field-name-field-reo-num-bathrooms').text.strip()

        rent_label = listing.find('h4', class_= 'label', string="Rent:")
        if rent_label:
            rent_div = rent_label.find_next('div', class_='value')
            rent_price = extract_price(rent_div.get_text(strip = True))

        furnished_label = listing.find('h4', class_= 'label', string= lambda text: "Furnished:")
        if furnished_label:
            furnished_div = furnished_label.find_next('div', class_='value')
            furnished_text = furnished_div.get_text(strip = True).lower()
            is_furnished = "yes" if "yes" in furnished_text else "no"
        else:
            is_furnished = "no"

        # Further filtering based on your criteria (price, bedrooms, availability)
        # This is a placeholder; you'll need to adjust logic based on actual listing details

        yield {
            'least_start': lease_start_date,
            'bedrooms': bedrooms,
            'bathrooms': bathrooms,
            'rent_price': rent_price,
            'furnished': is_furnished
        }

def get_listings():
    driver = get_driver()
    try:
        search_listings(driver)
        listings = list(parse_listings(driver))
        return listings
    finally:
        driver.quit()




if __name__ == '__main__':
    listings = get_listings()
    # Implement logic to filter listings based on requirements (2 bedrooms, 1 bath, < $2000, available in May or later)
    # The example provided does a general scrape; you will need to adjust parsing and filtering based on actual data and HTML structure
    for listing in listings:
        print(listing)