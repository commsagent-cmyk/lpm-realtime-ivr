import requests
from datetime import datetime
from flask import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# ==========
# MAKE.COM WEBHOOK URL (for button presses)
# ==========
MAKE_WEBHOOK_URL = "https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956"

# ==========
# PHONE NUMBERS
# ==========
NUM_AMY = "+13439619073"       # Reception
NUM_LYLA = "+13439976025"      # Urgent maintenance
NUM_MELISSA = "+13025968"      # Rentals follow-up, tenant billing
NUM_BERNARD = "+16132867190"   # Directory
NUM_STEPHANE = "+13439974344"  # Owners

# ==========
# VOICE
# ==========
DEFAULT_VOICE = "Polly.Aria-Neural"
DEFAULT_LANG = "en-US"

def say(resp: VoiceResponse, text: str):
    resp.say(text, voice=DEFAULT_VOICE, language=DEFAULT_LANG)

# ==========
# ROOT
# ==========
@app.get("/")
def home():
    return "LPM IVR is running!"

# ==========
# MAIN MENU: /voice
# ==========
@app.route("/voice", methods=["GET", "POST"])
def voice():
    r = VoiceResponse()

    # Log incoming call
    log_data = {
        "timestamp": datetime.utcnow().isoformat(),
        "caller_phone": request.form.get("From", "Unknown"),
        "Path": "Incoming",
        "Routed To": "Menu"
    }
    try:
        requests.post("https://hook.us2.make.com/r7v51fg3t0aw8hmwi0tdth4i0fmgq2cw", json=log_data, timeout=5)
    except:
        pass  # Silent fail

    # Ask for button → send to Make.com
    gather = Gather(
        num_digits=1,
        action=MAKE_WEBHOOK_URL,
        method="POST",
        timeout=6
    )
    say(gather,
        "Welcome to Larocque Property Management. "
        "Press 0 for reception. "
        "Press 9 for urgent maintenance. "
        "Press 1 for rentals. "
        "Press 2 for tenant support. "
        "Press 3 for owner inquiries. "
        "Press 4 for team directory."
    )
    r.append(gather)

    # No input
    say(r, "I didn't catch that.")
    r.redirect("/voice")

    return Response(str(r), mimetype="text/xml")

# ==========
# OPTIONAL: Keep old routes (safe to delete later)
# ==========
@app.route("/handle-main", methods=["POST"])
def handle_main():
    # This is now handled by Make.com — just hold music
    r = VoiceResponse()
    r.say("Please hold while we connect you...")
    r.play("http://com.twilio.sounds.music.s3.amazonaws.com/Masurka_op_7_no_1_-_3_4_time_scale.twilio.wav")
    return Response
