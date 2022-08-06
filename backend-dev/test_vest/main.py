import os
from flask import Flask, render_template, send_from_directory
from pywebcopy import save_website

APP_ROOT = os.path.dirname(os.path.abspath(__file__))
WEBSITE = "hackathon.bz.it"
URL = "https://" + WEBSITE

app = Flask(
    __name__,
    static_url_path='', 
    static_folder='websites/hackathon_site/' + WEBSITE)

def download_website():
    print("Started download of website: %s" %WEBSITE)
    FILENAME = "hackathon_site"
    FOLDER = APP_ROOT + "/websites"
    
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

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download', methods=['GET'])
def download():
    return send_from_directory("websites/hackathon_site/" + WEBSITE, "index.html")

if __name__ == "__main__":
    download_website()
    app.run(debug=True)