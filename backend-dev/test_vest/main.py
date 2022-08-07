from lib2to3.pgen2 import driver
import os, json
from flask import Flask, Response, render_template, send_from_directory, request
from flask_cors import CORS
from seleniumwire import webdriver
from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pywebcopy import save_website

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
WEBSITE = "hackathon.bz.it"
URL = "https://" + WEBSITE

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='hackathon_site/' + WEBSITE)
CORS(app)

def download_website():
    return save_website(
        url=URL,
        project_folder=APP_ROOT,
        project_name="hackathon_site",
        bypass_robots=True,
        debug=True,
        open_in_browser=True,
        delay=None,
        threaded=True,
   )

class website_scraper:
    def __init__(self, url):
        CHROME_DRIVER_PATH = "/Users/albertocrescini/Downloads/chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options, executable_path=CHROME_DRIVER_PATH)
        self.driver.get(url)
        self.accept_cookies()

    def accept_cookies(self):
        try:
            self.driver.find_element(by=By.XPATH, value='''//*[@id="pc-button"]/button''').click()
        except NoSuchElementException:
            pass

    def text_query(self, input: str, xpath=None):
        try:
            if xpath:
                element = self.wait_element_load(xpath)
                return input == element.get_attribute('innerText')
            else:
                return input in self.driver.page_source

        except NoSuchElementException:
            return False

    def wait_element_load(self, xpath: str):
        try:
            element = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, xpath)))
        except TimeoutException:
            return "Request timeout."
        return element

    def button_click(self, xpath: str):
        try:
            element = self.wait_element_load(xpath)
            element.click()
        except ElementClickInterceptedException:
            return "Element click intercepted: other element would receive the click."

    def check_redirect(self, expected_url: str, xpath: str):
        self.button_click(xpath)
        response = self.driver.current_url # was response=self.button_click(xpath)
        return response == expected_url
    
    def set_field(self, args: dict, submit_xpath: str):
        # mi aspetto {"key": "value"}
        for xpath, value in args.items():
            element = self.wait_element_load(xpath)
            element.send_keys(value)
        self.wait_element_load('//*[@id="_username"]').submit()

@app.route('/set_website_url', methods=['PUT'])
def set_website_url():
    args = request.args
    global URL, WEBSITE
    URL = args.get("url")
    WEBSITE = URL.split("://")[1]
    return json.dumps("Destination URL set: %s"%URL)

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory("hackathon_site/" + WEBSITE, "index.html")

@app.route('/test-scenario', methods=['POST'])
def test_case():
    scraper = website_scraper(URL)
    results = list()
    for tc in json.loads(request.data):
        try:
            if 'has' in tc:
                has = tc['has']
            else:
                has = None

            if 'page_url' in tc:
                page_url = tc['page_url']
            else:
                page_url = None

            if 'in' in tc:
                if 'element' in tc['in']:
                    element = tc['in']['element']
                else:
                    element = None
                if 'identified_by' in tc['in']:
                    identified_by = tc['in']['identified_by']
                else:
                    identified_by = None

            if 'after' in tc:
                action = tc['after']
            else:
                action = None

            if identified_by:
                if action == "clicked":
                    query_result = scraper.check_redirect(page_url, identified_by)
                    print(query_result)
                    results.append(query_result)
            
            if has:
                if identified_by:
                    query_result = scraper.text_query(has, identified_by)
                    results.append(query_result)
                    print(query_result)
                elif element == "page":
                    query_result = scraper.text_query(has)
                    results.append(query_result)
                    print(query_result)

                
            

        except KeyError as e:
            return Response("The specified key '%s' does not exist!"%e, status=404)
    return json.dumps(results)

if __name__ == "__main__":
    #download_website()
    app.run(host="localhost", debug=True)
    