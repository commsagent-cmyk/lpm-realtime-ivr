from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import requests
from datetime import datetime

from app import app  # import the Flask app we already have


@app.route("/voice", methods=["POST"])
def voice():
    r = VoiceResponse()
    r.say("Hello from Laroque Property Management. Your IVR connection is working.")

    # Prepare data to send to Make
    try:
        data = {
            "timestamp": datetime.utcnow().isoformat(),
            "caller_phone": request.values.get("From"),
            "caller_name": request.values.get("CallerName"),
            "Digits Pressed": request.values.get("Digits"),
            "Path": "Main Menu",
            "Routed To": "Pending"
        }
        # 🔗 Replace this with your actual Make webhook URL
        webhook_url = "https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956"
        requests.post(webhook_url, json=data)
    except Exception as e:
        print("Make webhook error:", e)

    return Response(str(r), mimetype="text/xml")
