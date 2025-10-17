from flask import Flask, Response
from twilio.twiml.voice_response import VoiceResponse
import os

app = Flask(__name__)

# Homepage — just for testing
@app.route("/")
def home():
    return "✅ LPM Realtime server is alive."

# Twilio voice webhook
@app.route("/voice", methods=["GET", "POST"])
def voice():
    r = VoiceResponse()
    r.say("Your IVR webhook is connected and responding. Hello from Larocque Property Management.")
    return Response(str(r), mimetype="text/xml")

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=port)
