import requests
from datetime import datetime

MAKE_WEBHOOK_URL = "https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956" 

def post_to_make(payload: dict):
    """Fire-and-forget webhook to Make."""
    try:
        requests.post(MAKE_WEBHOOK_URL, json=payload, timeout=5)
    except Exception as e:
        print("Make webhook error:", e)


from flask import Flask, Response, request
from twilio.twiml.voice_response import VoiceResponse, Gather
import os

app = Flask(__name__)

# ==========
# CONTACTS (replace with real E.164 numbers like +16135551234)
# ==========
NUM_AMY = "+13439619073"       # Reception, Rentals(1→1), Directory(1), 0
NUM_LYLA = "+13439976025"      # Tenants(2→1), Emergency(9), Directory(2)
NUM_MELISSA = "+13025968"   # Rentals(1→2), Tenants(2→2), Directory(3)
NUM_BERNARD = "+16132867190"   # Directory(4)
NUM_STEPHANE = "+13439974344"  # Owners(3→1), Directory(5)

# ==========
# VOICE (upgrade to a natural neural voice)
# Twilio supports Amazon Polly voices in <Say>. Good choices:
#   Polly.Aria-Neural (warm, modern) or Polly.Matthew-Neural (calm, male)
# ==========
DEFAULT_VOICE = "Polly.Aria-Neural"
DEFAULT_LANG = "en-US"

def say(resp: VoiceResponse, text: str):
    """Helper to keep voice consistent and clean."""
    resp.say(text, voice=DEFAULT_VOICE, language=DEFAULT_LANG)

# ----------
# Health / root
# ----------
@app.get("/")
def home():
    return "✅ LPM Realtime server is alive."

# ----------
# MAIN ENTRY: /voice (Twilio webhook)
# ----------
@app.route("/voice", methods=["GET", "POST"])
def voice():
    r = VoiceResponse()

    # --- Log call to Make webhook ---
    import requests, datetime
    make_webhook_url = "https://hook.us2.make.com/r7v51fg3t0aw8hmwi0tdth4i0fmgq2cw"  # <-- your real webhook URL
    call_data = {
        "timestamp": datetime.datetime.now().isoformat(),
        "caller_phone": request.form.get('From', 'Unknown'),
        "Digits Pressed": request.form.get('Digits', ''),
        "Path": "Main Menu",
        "Routed To": "Pending"
    }
    try:
        requests.post(make_webhook_url, json=call_data)
    except Exception as e:
        print("Error sending webhook:", e)
    # --------------------------------

    # Main menu (press any time)
    g = Gather(
        num_digits=1,
        action="/handle-main",
        timeout=6
    )
    say(g,
        "Welcome to Larocque Property Management. "
        "Our focus is your peace of mind. "
        "Please make a selection at any time. "
        "You can press 0 to reach reception. "
        "If you have an urgent maintenance issue, press 9. "
        "Press 1 if you're looking to rent a unit or need help with an application. "
        "Press 2 if you're a current tenant with a maintenance or account question. "
        "Press 3 if you're a property owner interested in management services for your investment property. "
        "Press 4 if you know the team member you'd like to reach."
    )
    r.append(g)

    # No input: repeat once
    say(r, "Sorry, I didn't catch that.")
    r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

# ----------
# MAIN HANDLER
# ----------
@app.route("/handle-main", methods=["POST"])
def handle_main():
    d = request.form.get("Digits", "")
    r = VoiceResponse()

    if d == "9":
        say(r, "Please hold. Your call will be directed immediately.")
        r.dial(NUM_LYLA)  # Urgent maintenance → Lyla
        return Response(str(r), mimetype="text/xml")

    if d == "1":
        g = Gather(num_digits=1, action="/rentals", timeout=6)
        say(g,
            "If you're calling about a property you saw online or want to learn how to apply, press 1. "
            "If you've already submitted an application and would like to follow up, press 2."
        )
        r.append(g)
        say(r, "Sorry, I didn't catch that.")
        r.redirect("/voice")
        return Response(str(r), mimetype="text/xml")

    if d == "2":
        g = Gather(num_digits=1, action="/tenants", timeout=6)
        say(g,
            "For maintenance or repairs, press 1. "
            "For rent, billing, or account questions, press 2."
        )
        r.append(g)
        say(r, "Sorry, I didn't catch that.")
        r.redirect("/voice")
        return Response(str(r), mimetype="text/xml")

    if d == "3":
        g = Gather(num_digits=1, action="/owners", timeout=6)
        say(g, "If you'd like to speak with someone about management services for your property, press 1.")
        r.append(g)
        say(r, "Sorry, I didn't catch that.")
        r.redirect("/voice")
        return Response(str(r), mimetype="text/xml")

    if d == "4":
        g = Gather(num_digits=1, action="/directory", timeout=8)
        say(g,
            "To reach a team member directly, choose from the following options. "
            "Press 1 for Amy. "
            "Press 2 for Lyla. "
            "Press 3 for Melissa. "
            "Press 4 for Bernard. "
            "Press 5 for Stephane."
        )
        r.append(g)
        say(r, "Sorry, I didn't catch that.")
        r.redirect("/voice")
        return Response(str(r), mimetype="text/xml")

    if d == "0":
        say(r, "Transferring you to reception.")
        r.dial(NUM_AMY)
        return Response(str(r), mimetype="text/xml")

    # Invalid
    say(r, "Sorry, I didn't catch that.")
    r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

# ----------
# SUB-MENUS
# ----------
@app.route("/rentals", methods=["POST"])
def rentals():
    d = request.form.get("Digits", "")
    r = VoiceResponse()
    if d == "1":
        say(r, "Connecting you now.")
        r.dial(NUM_AMY)
    elif d == "2":
        say(r, "Connecting you now.")
        r.dial(NUM_MELISSA)
    else:
        r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

@app.route("/tenants", methods=["POST"])
def tenants():
    d = request.form.get("Digits", "")
    r = VoiceResponse()
    if d == "1":
        say(r, "Connecting you now.")
        r.dial(NUM_LYLA)
    elif d == "2":
        say(r, "Connecting you now.")
        r.dial(NUM_MELISSA)
    else:
        r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

@app.route("/owners", methods=["POST"])
def owners():
    d = request.form.get("Digits", "")
    r = VoiceResponse()
    if d == "1":
        say(r, "Connecting you now.")
        r.dial(NUM_STEPHANE)
    else:
        r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

@app.route("/directory", methods=["POST"])
def directory():
    d = request.form.get("Digits", "")
    r = VoiceResponse()
    directory_map = {
        "1": NUM_AMY,
        "2": NUM_LYLA,
        "3": NUM_MELISSA,
        "4": NUM_BERNARD,
        "5": NUM_STEPHANE,
    }
    if d in directory_map:
        say(r, "Connecting you now.")
        r.dial(directory_map[d])
    else:
        r.redirect("/voice")
    return Response(str(r), mimetype="text/xml")

@app.route("/testwebhook")
def test_webhook():
    import requests
    r = requests.post("https://hook.us2.make.com/3jyuecix8qbipfkeyxawtzwy70grm956", json={"test": "ping"})
    return f"Make.com returned {r.status_code}"


# ----------
# RUN (Render provides PORT env)
# ----------
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
