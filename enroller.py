import time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

email_link_to_enroll = 'http://links.illinois.edu/THE_LINK_TO_ENROLL_IN_COURSES'
creds = ('your_username', 'your_password')
crn = '12345' # Course identifier
chrome_driver_path = "C:\\path\\to\\chromedriver.exe" # From https://chromedriver.chromium.org/downloads

timeout_per_step = 10

def wait_and_get(driver, how, what):
    return WebDriverWait(driver, timeout_per_step).until(EC.visibility_of_element_located((how, what)))

def wait_until_title_is(driver, title):
    WebDriverWait(driver, timeout_per_step).until(EC.title_contains(title))

def enroll():
    driver = webdriver.Chrome(executable_path=chrome_driver_path)
    driver.get(email_link_to_enroll)
    
    if 'Login' in driver.title:
        wait_and_get(driver, By.NAME, "USER").send_keys(creds[0])
        wait_and_get(driver, By.NAME, "PASSWORD").send_keys(creds[1])
        wait_and_get(driver, By.NAME, "BTN_LOGIN").click()

    wait_until_title_is(driver, 'Registration')
    wait_and_get(driver, By.ID, "registerLink").click()

    wait_until_title_is(driver, 'Select')
    print('Selecting term...')
    wait_and_get(driver, By.CLASS_NAME, "select2-choice").click()
    wait_and_get(driver, By.CLASS_NAME, "select2-result").click() # Selects latest term
    wait_and_get(driver, By.ID, "term-go").click()

    wait_until_title_is(driver, 'Registration')
    print('Entering CRN...')
    wait_and_get(driver, By.ID, "enterCRNs-tab").click()
    wait_and_get(driver, By.ID, "txt_crn1").send_keys(crn)

    wait_and_get(driver, By.ID, "addCRNbutton").click()

    print('Submitting...')
    wait_and_get(driver, By.ID, "saveButton").click()

    driver.close()

if __name__ == '__main__':
    enroll()