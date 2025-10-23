from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests
from datetime import datetime

from app import app  # Keep this if you're using the same app

@app.route("/voice", methods=["POST"])
def voice():
    r = VoiceResponse()

    # --- Say welcome ---
    r.say("Welcome to Larocque Property Management.", voice="Polly.Aria-Neural")

    # --- Ask to press a button AND send it to Make.com ---
    gather = Gather(
        num_digits=1,
        action="https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956",  # Fixed URL
        method="POST",
        timeout=5
    )
    gather.say(
        "Press 0 for reception. "
        "Press 9 for urgent maintenance. "
        "Press 1 for rentals. "
        "Press 2 for tenant support. "
        "Press 3 for owner inquiries. "
        "Press 4 for team directory.",
        voice="Polly.Aria-Neural"
    )
    r.append(gather)

    # --- If no press: repeat ---
    r.say("I didn't catch that.")
    r.redirect("/voice")

    # --- Log the incoming call to Make.com ---
    data = {
        "timestamp": datetime.utcnow().isoformat(),
        "caller_phone": request.values.get("From"),
        "caller_name": request.values.get("CallerName"),
        "Digits Pressed": "",  # Will be filled on next request
        "Path": "Incoming Call",
        "Routed To": "Menu"
    }

    webhook_url = "https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956"
    try:
        requests.post(webhook_url, json=data, timeout=5)
        print("Webhook sent: Incoming call logged")
    except Exception as e:
        print("Webhook error:", e)

    return Response(str(r), mimetype="text/xml")
