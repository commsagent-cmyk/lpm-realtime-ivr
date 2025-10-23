from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import requests
from datetime import datetime

# Create a new Flask app just for this file
app = Flask(__name__)

# ==========
# MAKE.COM WEBHOOK (button presses go here)
# ==========
MAKE_WEBHOOK_URL = "https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956"

# ==========
# MAIN MENU: /voice
# ==========
@app.route("/voice", methods=["GET", "POST"])
def voice():
    r = VoiceResponse()

    # Log incoming call to Make.com
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "caller_phone": request.values.get("From", "Unknown"),
        "Path": "Incoming Call",
        "Routed To": "Menu"
    }
    try:
        requests.post("https://hook.us2.make.com/r7v51fg3t0aw8hmwi0tdth4i0fmgq2cw", json=log_data, timeout=5)
    except:
        pass  # Don't crash if webhook fails

    # Ask caller to press a button → send to Make.com
    gather = Gather(
        num_digits=1,
        action=MAKE_WEBHOOK_URL,
        method="POST",
        timeout=6
    )
    gather.say(
        "Welcome to Larocque Property Management. "
        "Press 0 for reception. "
        "Press 9 for urgent maintenance. "
        "1 for rentals. "
        "2 for tenant support. "
        "3 for owner inquiries. "
        "4 for team directory.",
        voice="Polly.Aria-Neural"
    )
    r.append(gather)

    # If no input
    r.say("I didn't catch that.")
    r.redirect("/voice")

    return Response(str(r), mimetype="text/xml")

# ==========
# RUN THE SERVER
# ==========
if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
