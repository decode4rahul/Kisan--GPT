from twilio.rest import Client
from twilio.twiml import VoiceResponse
from flask import Flask, request
import os
from ai import *

app = Flask(__name__)

# Twilio credentials
TWILIO_SID = os.getenv("TWILIO_SID")
TWILIO_TOKEN = os.getenv("TWILIO_TOKEN")
client = Client(TWILIO_SID, TWILIO_TOKEN)

@app.route("/voice", methods=['POST'])
def handle_call():
    """Handle incoming voice calls"""
    response = VoiceResponse()
    
    # Reset conversation for new caller
    reset_conversation()
    
    # Welcome message
    response.say("Hello! I am your farming assistant. Please tell me your name and farming problem.", 
                voice='alice', language='en-IN')
    
    # Gather speech input
    gather = response.gather(
        input='speech',
        action='/process_speech',
        speech_timeout='auto',
        language='hi-IN'  # Hindi support
    )
    
    return str(response)

@app.route("/process_speech", methods=['POST'])
def process_speech():
    """Process farmer's speech input"""
    response = VoiceResponse()
    
    # Get speech text from Twilio
    speech_result = request.form.get('SpeechResult', '')
    
    if speech_result:
        # Add to conversation history
        conversation_history.append({"role": "user", "content": speech_result})
        
        # Get AI response using your chat function
        bot_reply = chat_with_farmer(speech_result)
        
        # Speak the response
        response.say(bot_reply, voice='alice', language='hi-IN')
        
        # Continue conversation
        gather = response.gather(
            input='speech',
            action='/process_speech',
            speech_timeout='auto',
            language='hi-IN'
        )
    else:
        response.say("I didn't catch that. Please speak again.", voice='alice')
        response.redirect('/voice')
    
    return str(response)

if __name__ == "__main__":
    app.run(debug=True, port=5000)