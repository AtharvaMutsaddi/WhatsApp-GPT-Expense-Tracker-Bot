import requests, os
from dotenv import load_dotenv
from constants import WATSON_ACCESS_TOKEN_POST_ENDPOINT
from config import WATSON_CLOUD_API_KEY
load_dotenv()


def getAccessToken() -> str:
    data = {
        "grant_type": "urn:ibm:params:oauth:grant-type:apikey",
        "apikey": WATSON_CLOUD_API_KEY,
    }
    response = requests.post(
        WATSON_ACCESS_TOKEN_POST_ENDPOINT,
        headers={"Content-Type": "application/x-www-form-urlencoded"},
        data=data,
    )

    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]
    else:
        print("Error:", response.status_code, response.text)