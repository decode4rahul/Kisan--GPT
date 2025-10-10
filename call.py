from flask import Flask, request, Response
from ai import chat_with_ai, reset_conversation  # Your AI functions

app = Flask(__name__)

# Track conversation per call
call_sessions = {}

@app.route("/voice", methods=["POST"])
def voice():
    """Handle incoming call and start conversation."""
    call_sid = request.form.get("CallSid")
    call_sessions[call_sid] = {"history": []}

    reset_conversation()  # reset AI context for new call

    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-US">Hello! I am your farming assistant. Please tell me your name.</Say>
    <Gather input="speech" action="/gather" method="POST" language="en-US" speechTimeout="auto"/>
</Response>"""
    return Response(twiml, mimetype="text/xml")


@app.route("/gather", methods=["POST"])
def gather():
    """Receive text from Twilio speech recognition, send to AI, and respond."""
    call_sid = request.form.get("CallSid")
    user_speech = request.form.get("SpeechResult", "").strip()
    print(user_speech)
    if call_sid not in call_sessions:
        call_sessions[call_sid] = {"history": []}
        reset_conversation()

    if not user_speech:
        # No speech detected, prompt again
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-US">Sorry, I didn't catch that. Please say it again.</Say>
    <Gather input="speech" action="/gather" method="POST" language="en-US" speechTimeout="auto"/>
</Response>"""
        return Response(twiml, mimetype="text/xml")

    # Send farmer speech to AI
    ai_reply = chat_with_ai(user_input=user_speech)
    print(ai_reply)
    # Log conversation
    call_sessions[call_sid]["history"].append({"farmer": user_speech, "ai": ai_reply})

    # Respond with AI reply and gather again for next turn
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="alice" language="en-US">{ai_reply}</Say>
    <Gather input="speech" action="/gather" method="POST" language="en-US" speechTimeout="auto"/>
</Response>"""
    return Response(twiml, mimetype="text/xml")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)
