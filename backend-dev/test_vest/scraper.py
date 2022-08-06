from selenium.common.exceptions import (ElementClickInterceptedException,
                                        NoSuchElementException,
                                        TimeoutException)
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from seleniumwire import webdriver

options = webdriver.ChromeOptions()
# options.headless = True

CHROME_DRIVER_PATH = "/Users/albertocrescini/Downloads/chromedriver"
URL = "https://hackathon.bz.it"

driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

driver.get(URL)

# IGNORE COOKIES:
driver.find_element(by=By.XPATH,
                    value='''//*[@id="pc-button"]/button''').click()


def text_research(input: str, xpath=None):
    try:
        if xpath:
            element = driver.find_element(by=By.XPATH, value=xpath)
            return input == element.get_attribute('innerText')
        else:
            return input in driver.page_source

    except NoSuchElementException:
        return "Unable to find xpath: %s" % xpath


def wait_element_load(xpath: str):
    try:
        element = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath)))
    except TimeoutException:
        return "Request timeout."
    return element


def button_click(xpath: str):
    try:
        element = wait_element_load(xpath)
        element.click()
    except ElementClickInterceptedException:
        return "Some other element would receive the click."


print(text_research("NOI Hackathon Summer Edition"))
print(
    text_research("Read more", '''//*[@id="coming-soon"]/div/div/div/div/a'''))
print(wait_element_load('''//*[@id="coming-soon"]/div/div/div/div/a'''))
print(button_click('''/html/body/footer/div[2]/div[5]/p/a'''))
