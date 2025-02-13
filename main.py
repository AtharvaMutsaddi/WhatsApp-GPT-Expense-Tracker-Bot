from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
app = Flask(__name__)
from db import *
from llm import Agent
from config import OPENAI_API_KEY

wa_agent=Agent(OPENAI_API_KEY)

@app.route('/whatsapp', methods=['GET','POST'])
def receive_message():
    sender = request.form.get('From')
    message = request.form.get('Body')

    print(f"Message: {message}")
    prompt=f"{message}. Phone number: {sender}"
    llm_res=wa_agent.run_conversation(prompt)
    response=MessagingResponse()
    response.message(llm_res)
    
    return str(response)

if __name__ == '__main__':
    setup_database()
    app.run(port=8080, debug=True)
