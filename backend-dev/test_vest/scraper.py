from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywebcopy import save_website

options = webdriver.ChromeOptions()
# options.headless = True

CHROME_DRIVER_PATH = "/Users/albertocrescini/Downloads/chromedriver"
#URL = "https://hackathon.bz.it"
URL = "https://hackathon.bz.it/secure/login"

driver = webdriver.Chrome(options=options, executable_path=CHROME_DRIVER_PATH)

driver.get(URL)

def accept_cookies():
    try:
        driver.find_element(by=By.XPATH, value='''//*[@id="pc-button"]/button''').click()
    except NoSuchElementException:
        pass

def text_research(input: str, xpath=None):
    try:
        if xpath:
            element = wait_element_load(xpath)
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
        return "Element click intercepted: other element would receive the click."

def set_field(args: dict, submit_xpath: str):
    # mi aspetto {"key": "value"}
    for xpath, value in args.items():
        element = wait_element_load(xpath)
        element.send_keys(value)
    wait_element_load('//*[@id="_username"]').submit()

def download_website():
    FILENAME = "hackathon_site"
    FOLDER = "/Users/albertocrescini/Desktop/nhse-2022/backend-dev/template"
    
    return save_website(
        url=URL,
        project_folder=FOLDER,
        project_name=FILENAME,
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=True,
    )
    
accept_cookies()
print(text_research("NOI Hackathon Summer Edition"))
print(
    text_research("Read more", '''//*[@id="coming-soon"]/div/div/div/div/a'''))
print(wait_element_load('''//*[@id="coming-soon"]/div/div/div/div/a'''))
print(button_click('''/html/body/footer/div[2]/div[5]/p/a'''))
set_field({
    '//*[@id="_username"]': 'value1',
    '//*[@id="_password"]': 'value2'
}, submit_xpath='//*[@id="_submit"]')