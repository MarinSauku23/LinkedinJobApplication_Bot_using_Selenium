from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import time
import os

ACCOUNT_EMAIL = os.environ.get("EMAIL")
ACCOUNT_PASSWORD = os.environ.get("PASSWORD")
PHONE = os.environ.get("PHONE")


def abort_application():
    # Click Close Button
    close_button = driver.find_element(By.CLASS_NAME, value="artdeco-modal__dismiss")
    close_button.click()

    time.sleep(2)
    # Click Discard Button
    discard_button = driver.find_elements(By.CLASS_NAME, value="artdeco-modal__confirm-dialog-btn")[1]
    discard_button.click()


chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("detach", True)

driver = webdriver.Chrome(options=chrome_options)

driver.get("https://www.linkedin.com/jobs/search/?f_LF=f_AL&geoId=102257491"
            "&keywords=python%20developer"
            "&location=London%2C%20England%2C%20United%20Kingdom"
            "&redirect=false&position=1&pageNum=0")

# Click Reject Cookies Button
time.sleep(2)
reject_button = driver.find_element(By.CSS_SELECTOR, value='button[action-type="DENY"]')
reject_button.click()

# Click Sign in Button
time.sleep(2)
sign_in_button = driver.find_element(By.LINK_TEXT, value="Sign in")
sign_in_button.click()

# Sign in
time.sleep(5)
email_field = driver.find_element(By.ID, value="username")
email_field.send_keys(ACCOUNT_EMAIL)
password_field = driver.find_element(By.ID, value="password")
password_field.send_keys(ACCOUNT_PASSWORD)
password_field.send_keys(Keys.ENTER)

# CAPTCHA - Solve Puzzle Manually
input("Press Enter when you have solved the Captcha")

# Get Listing
time.sleep(5)
all_listing = driver.find_elements(By.CSS_SELECTOR, value=".job-card-container--clickable")

# Apply for jobs
for listing in all_listing:
    print("Opening Listing")
    listing.click()
    time.sleep(2)
    try:
        # Click Apply Button
        apply_button = driver.find_element(By.CSS_SELECTOR, value=".jobs-s-apply button")
        apply_button.click()

        # Insert phone number
        # Find an <input> element where the id contains phoneNumber
        time.sleep(5)
        phone = driver.find_element(By.CSS_SELECTOR, value="input[id*=phoneNumber]")
        if phone.text == "":
            phone.send_keys(PHONE)

        # Check the submit button
        submit_button = driver.find_element(By.CSS_SELECTOR, value="footer button")
        if submit_button.get_attribute("data-control-name") == "continue_unify":
            abort_application()
            print("Complex application, skipped.")
            continue
        else:
            print("Submitting job application.")
            submit_button.click()

        time.sleep(2)
        # Click Close Button
        close_button = driver.find_element(By.CSS_SELECTOR, value="artdeco-modal__dismiss")
        close_button.click()

    except NoSuchElementException:
        abort_application()
        print("No application button, skipped.")
        continue

time.sleep(5)
driver.quit()

