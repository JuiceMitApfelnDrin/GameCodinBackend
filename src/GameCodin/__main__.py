from dotenv import load_dotenv
load_dotenv('./env/.env')

from . import app

if __name__ == "__main__":
    app.start()