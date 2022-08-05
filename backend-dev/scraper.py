from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By

options = webdriver.ChromeOptions()
options.headless = True

CHROME_DRIVER_PATH = "/Users/albertocrescini/Downloads/chromedriver"
URL = "https://hackathon.bz.it"

driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)
driver.get(URL)

def text_research(input: str, xpath=None):
    try:
        if xpath:
            element = driver.find_element(by=By.XPATH, value=xpath)
            return input == element.get_attribute('innerText')
        else:
            return input in driver.page_source
    except NoSuchElementException:
        print("Unable to find xpath: %s"%xpath)

#coming-soon > div > div > div > div > a
#print(text_research("NOI Hackathon Summer Edition"))
print(text_research("Read more", '''//*[@id="coming-soon"]/div/div/div/div/a'''))