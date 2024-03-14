from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def get_driver():
    service = Service('***********')
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    options.add_argument('--no-sandbox')  # Bypass OS security model
    options.add_argument('start-maximized')  #
    options.add_argument('disable-infobars')
    options.add_argument('--disable-extensions')
    driver = webdriver.Chrome(service=service, options=options)
    return driver


def login_to_site(driver, username, password, login_url, username_field_id, password_field_id, submit_button_id):
    """
    Logs into a site using provided credentials.
    """
    driver.get(login_url)
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, username_field_id)))

    driver.find_element(By.ID, username_field_id).send_keys(username)
    driver.find_element(By.ID, password_field_id).send_keys(password)
    driver.find_element(By.ID, submit_button_id).click()

    # Wait for login to complete; adjust based on the page or element to wait for
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'body')))

def fill_form_with_details(driver, form_details, form_url):
    """
    Navigates to the form page after login and fills out the form.
    """
    # Navigate to the form page
    driver.get(form_url)

    # Wait for the form to be ready; adjust selector as needed
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, 'form')))

    # Example of filling a specific field; adjust based on actual field IDs or names
    driver.find_element(By.ID, 'field_id').send_keys(form_details['field_value'])

    # Fill other fields as required

    # Submit the form
    submit_button = driver.find_element(By.ID, 'submit_button_id')  # Adjust the ID accordingly
    submit_button.click()

    # Optionally, confirm submission was successful
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, 'success_message_class')))  # Adjust the class name accordingly

def main(username, password):
    driver = get_driver()
    try:
        # Log in
        login_to_site(driver, username, password, "https://realestate.dartmouth.edu/dartmouth-rentals", "*******", "*********", "login_button_id")

        # Fill out and submit the form
        form_details = {
            'field_value': 'Some value',  # Example field value
            # Add other form details as necessary
        }
        fill_form_with_details(driver, form_details, "https://realestate.dartmouth.edu/dartmouth-rentals")

        print("Form submitted successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        driver.quit()

if __name__ == "__main__":
    USERNAME = '********'
    PASSWORD = '*******'
    main(USERNAME, PASSWORD)


'''
THIS IS FOR TESTING WHETHER THE WEBSITE CAN BE REACHED

def open_website(url):
    # Initialize the driver
    driver = get_driver()
    # Navigate to the specified URL
    driver.get(url)
    
    # Optional: wait for a specific element to ensure the page has loaded
    # WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, 'element_id')))

    # Print the title to ensure we've opened the correct page
    print(f"The title of the page is: {driver.title}")
    
    # Close the browser
    driver.quit()

# Replace 'https://example.com' with the URL you wish to access
TARGET_URL = 'https://realestate.dartmouth.edu/dartmouth-rentals'

if __name__ == "__main__":
    open_website(TARGET_URL)
'''
