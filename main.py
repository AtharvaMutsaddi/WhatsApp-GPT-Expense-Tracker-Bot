from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from db import *
from llm import Agent
from config import OPENAI_API_KEY, TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN
from cv import make_ocr_request
import requests
import os

wa_agent=Agent(OPENAI_API_KEY)

@app.route('/whatsapp', methods=['GET','POST'])
def receive_message():
    print(request.form)
    sender = request.form.get('From')
    message = request.form.get('Body')
    media_url = request.form.get('MediaUrl0')
    prompt=f"{message}. Phone number: {sender}"
    if media_url:
        r = requests.get(media_url, auth=(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN))
        content_type = r.headers['Content-Type']
        username = sender.split(':')[1]
        ext = None
        if content_type == 'image/jpeg':
            ext = 'jpg'
        elif content_type == 'image/png':
            ext = 'png'
        
        if ext:
            save_dir = f'uploads/{username}'
            os.makedirs(save_dir, exist_ok=True)  # Create directory if not exists
            filename = f'{save_dir}/{username}.{ext}'

            with open(filename, 'wb') as f:
                f.write(r.content)

            # Extract text from image
            extracted_text = make_ocr_request(filename)
            prompt=f"{message}. Phone number: {sender}. An image was sent. Extracted text from the image: {extracted_text}"
    
    print(f"Message: {message}")
    llm_res=wa_agent.run_conversation(prompt)
    response=MessagingResponse()
    response.message(llm_res)
    
    return str(response)

if __name__ == '__main__':
    setup_database()
    app.run(port=8080, debug=True)
