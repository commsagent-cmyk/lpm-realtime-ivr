from flask import Flask, request, Response
from twilio.twiml.voice_response import VoiceResponse

from app import app  # import the Flask app we already have

@app.route("/voice", methods=["POST"])
def voice():
    r = VoiceResponse()
    r.say("Hello from Larocque Property Management. Your IVR connection is working.")
    return Response(str(r), mimetype="text/xml")
