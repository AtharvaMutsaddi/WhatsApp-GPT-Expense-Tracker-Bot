import os
from dotenv import load_dotenv

load_dotenv()

TWILIO_ACCOUNT_SID = os.getenv("TWILIO_ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.getenv("TWILIO_AUTH_TOKEN")
TWILIO_WHATSAPP_NUMBER = os.getenv("TWILIO_WA_BOT_PHONENUMBER")
MY_NUMBER=os.getenv("MY_PHONENUMBER")
OPENAI_API_KEY=os.getenv("OPENAI_API_KEY")
