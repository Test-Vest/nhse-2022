import os

from vest_test.main import app
from waitress import serve

if __name__ == "__main__":
    serve(app, host="0.0.0.0", port=os.environ.get("PORT") or 8080)
