from flask import Flask, request
import openai
from twilio.rest import Client

app = Flask(__name__)

# Use environment variables (set later in Render)
import os
openai.api_key = os.getenv("OPENAI_API_KEY")
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
twilio_number = os.getenv("TWILIO_NUMBER")

client = Client(account_sid, auth_token)

@app.route("/missed-call-check", methods=["POST"])
def missed_call():
    call_status = request.form.get("DialCallStatus")
    from_number = request.form.get("From")

    if call_status in ['no-answer', 'busy', 'failed']:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are helping Igor sell a 2014 Nissan Versa."},
                {"role": "user", "content": "Someone just called but missed Igor. Send a polite follow-up text but keep it short and sweet."}
            ]
        )
        reply_text = response['choices'][0]['message']['content']

        client.messages.create(
            body=reply_text,
            from_=twilio_number,
            to=from_number
        )

    return "<Response></Response>"