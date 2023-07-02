import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select

def automate_survey_junkie(email, password):
    # Set up Selenium WebDriver
    driver = webdriver.Chrome()
    driver.get("https://www.surveyjunkie.com/")

    # Log in to your Survey Junkie account
    login_email_field = driver.find_element(By.ID, "login-email")
    login_email_field.send_keys(email)

    login_password_field = driver.find_element(By.ID, "login-password")
    login_password_field.send_keys(password)

    login_button = driver.find_element(By.ID, "login-submit")
    login_button.click()

    # Wait for the login to complete
    time.sleep(2)

    # Navigate to the survey page
    driver.get("https://www.surveyjunkie.com/your-surveys")

    # Iterate through the surveys and complete them
    surveys = driver.find_elements(By.CSS_SELECTOR, ".survey-link")
    for survey in surveys:
        survey.click()

        # Wait for the survey to load
        time.sleep(3)

        # Complete the survey by selecting options or entering text
        # Add code here to interact with the survey elements, such as selecting options or entering text
        options = driver.find_elements(By.CSS_SELECTOR, ".survey-option")
        for option in options:
            option.click()

        text_fields = driver.find_elements(By.CSS_SELECTOR, ".survey-text")
        for text_field in text_fields:
            text_field.send_keys("Sample text")

        # Submit the survey
        submit_button = driver.find_element(By.CSS_SELECTOR, ".survey-submit-button")
        submit_button.click()

        # Wait for the next survey to load
        time.sleep(2)

    # Close the browser window
    driver.quit()

# Enter your Survey Junkie credentials
email = "your_email@example.com"
password = "your_password"

# Run the automation script
automate_survey_junkie(email, password)
