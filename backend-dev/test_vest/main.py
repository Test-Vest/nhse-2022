import os, json
from flask import Flask, Response, render_template, send_from_directory, request
from pywebcopy import save_website

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
    static_folder='websites/hackathon_site/' + WEBSITE)

class website_scraper:
    def __init__(self):
        CHROME_DRIVER_PATH = "/Users/albertocrescini/Downloads/chromedriver"
        self.options = webdriver.ChromeOptions()
        self.options.headless = True
        self.driver = webdriver.Chrome(options=self.options, executable_path=CHROME_DRIVER_PATH)
        self.driver.get(URL)
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
            return "Unable to find xpath: %s" % xpath

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

    def set_field(self, args: dict, submit_xpath: str):
        # mi aspetto {"key": "value"}
        for xpath, value in args.items():
            element = wait_element_load(xpath)
            element.send_keys(value)
        self.wait_element_load('//*[@id="_username"]').submit()

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
        
    """
    print(text_query("NOI Hackathon Summer Edition"))
    print(text_query("Read more", '''//*[@id="coming-soon"]/div/div/div/div/a'''))
    print(wait_element_load('''//*[@id="coming-soon"]/div/div/div/div/a'''))
    print(button_click('''/html/body/footer/div[2]/div[5]/p/a'''))
    set_field({
        '//*[@id="_username"]': 'value1',
        '//*[@id="_password"]': 'value2'
    }, submit_xpath='//*[@id="_submit"]')
    """

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory("websites/hackathon_site/" + WEBSITE, "index.html")

@app.route('/test_case', methods=['GET'])
def test_case():
    scraper = website_scraper()
    results = list()
    for tc in json.loads(request.data):
        try:
            if 'has' in tc:
                has = tc['has']
            else:
                has = None
            if 'in' in tc:
                if 'element' in tc:
                    element = tc['in']['element']
                else:
                    element = None
                if 'identified_by' in tc:
                    identified_by = tc['in']['identified_by']
                else:
                    identified_by = None
            if 'after' in tc:
                action = tc['after']
            else:
                action = None

            if action == "clicked":
                scraper.button_click(identified_by)
            query_result = scraper.text_query(has, identified_by)
            results.append(query_result)
            print(query_result)


        except KeyError as e:
            return Response("The specified key '%s' does not exist!"%e, status=404)
    return json.dumps(results)

if __name__ == "__main__":
    #download_website()
    app.run(debug=True)
    