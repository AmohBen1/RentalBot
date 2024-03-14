from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from website.form_filler import *

def automate_form_submission(form_url, username, password, form_data):
    # Initialize WebDriver
    driver = webdriver.Chrome(executable_path='/path/to/chromedriver')

    # Navigate to the form's URL
    driver.get(form_url)

    # Log in
    driver.find_element(By.ID, 'username_field_id').send_keys(username)
    driver.find_element(By.ID, 'password_field_id').send_keys(password)
    driver.find_element(By.ID, 'login_button_id').click()

    # Wait for login to complete and navigate to the form page if necessary
    # Fill out the form using form_data
    # Example:
    driver.find_element(By.ID, 'example_field_id').send_keys(form_data['example'])

    # Submit the form
    driver.find_element(By.ID, 'submit_button_id').click()

    # Close the WebDriver
    driver.quit()

def main(username, password):
    driver = get_driver()
    try:
        # Log in
        login_to_site(driver, username, password, "https://realestate.dartmouth.edu/dartmouth-rentals", "benjamin.k.amoh.th@dartmouth.edu", "Elyon@jehowa0", "login_button_id")

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
    USERNAME = 'benjamin.k.amoh.th@dartmouth.edu'
    PASSWORD = 'Elyon@jehowa0'
    main(USERNAME, PASSWORD)
