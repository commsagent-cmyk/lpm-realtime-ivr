from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse
import requests
from datetime import datetime

from app import app  # import the Flask app we already have


@app.route("/voice", methods=["POST"])
def voice():
    r = VoiceResponse()
    print("📞 Incoming call received:", request.values)
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
  webhook_url = "https://hook.us2.make.com/j3yueciix8qibpfkeyxawtzwy70grm956"

try:
    headers = {"Content-Type": "application/json"}
response = requests.post(webhook_url, json=data, headers=headers, timeout=10)
print("✅ Webhook sent to Make:", response.status_code, response.text, data)

except Exception as e:
    print("❌ Error sending webhook:", e)


    return Response(str(r), mimetype="text/xml")
