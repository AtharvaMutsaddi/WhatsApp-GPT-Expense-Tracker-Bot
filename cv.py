import requests, base64, os, time, re
from pathlib import Path
from utils.accessToken import getAccessToken
from constants import (
    WATSON_PROMPT_LAB_URL,
    WATSON_VISION_MODEL_PROMPT,
    WATSON_VISION_MODEL_ID,
)
from config import (
    WATSONX_PROJECT_ID,
)
from dotenv import load_dotenv

load_dotenv()


def get_type_of_image(image_path: str) -> str:
    path = Path(image_path)
    return path.suffix


def image_to_base64(image_path):
    with open(image_path, "rb") as image_file:
        image_data = image_file.read()
        base64_encoded_data = base64.b64encode(image_data)
        base64_string = base64_encoded_data.decode("utf-8")
        return base64_string


def make_ocr_request(img_path: str) -> str:
    body = {
        "messages": [
            {
                "role": "user",
                "content": [
                    {
                        "type": "text",
                        "text": WATSON_VISION_MODEL_PROMPT,
                    },
                    {
                        "type": "image_url",
                        "image_url": {
                            "url": f"""data:image/{get_type_of_image(img_path)};base64,{image_to_base64(img_path)}"""
                        },
                    },
                ],
            }
        ],
        "project_id": WATSONX_PROJECT_ID,
        "model_id": WATSON_VISION_MODEL_ID
    }

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": f"""Bearer {getAccessToken()}""",
    }

    response = requests.post(WATSON_PROMPT_LAB_URL, headers=headers, json=body)

    if response.status_code != 200:
        raise Exception("Non-200 response: " + str(response.text))

    data = response.json()

    resContent = data["choices"][0]["message"]["content"]
    ingreds = resContent.split(",")
    cleanedIngreds = []
    for ingred in ingreds:
        ingred = ingred.replace("'", "").strip()
        cleanedIngreds.append(ingred)

    return cleanedIngreds