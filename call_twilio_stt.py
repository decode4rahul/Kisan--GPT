from flask import Flask, request, Response
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(api_key="open ai api key")

# Store conversations
conversations = {}

def chat_with_gpt(messages):
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7,
            max_tokens=100  # Keep short for voice
        )
        return response.choices[0].message.content.strip()
    except:
        return "क्षमा करें, कुछ समस्या है।"

@app.route("/", methods=["GET", "POST"])
def handle_call():
    call_sid = request.values.get("CallSid")
    
    # Initialize conversation
    conversations[call_sid] = [
        {
            "role": "system",
            "content": """You are a helpful AI assistant for Indian farmers. 

Answer ANY question naturally - farming problems, general questions, casual chat, anything.

For farming: Give practical solutions with medicine names and prices.
Keep responses very short (1-2 sentences) for voice calls.
Respond in Hindi/English mix naturally.
Be friendly and conversational."""
        }
    ]
    
    twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="hi-IN">नमस्ते! मैं आपका AI सहायक हूँ। आप कुछ भी पूछ सकते हैं।</Say>
    <Gather input="speech" action="/process" method="POST" language="hi-IN,en-US" speechTimeout="5" timeout="10"/>
</Response>"""
    
    return Response(twiml, mimetype="text/xml")

@app.route("/process", methods=["POST"])
def process():
    call_sid = request.form.get("CallSid")
    user_speech = request.form.get("SpeechResult", "").strip()
    
    print(f"Twilio heard: '{user_speech}'")
    
    if call_sid not in conversations:
        return handle_call()
    
    if not user_speech or len(user_speech) < 2:
        twiml = """<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="hi-IN">मैं समझ नहीं पाया। कृपया दोबारा कहें।</Say>
    <Gather input="speech" action="/process" method="POST" language="hi-IN,en-US" speechTimeout="5" timeout="10"/>
</Response>"""
        return Response(twiml, mimetype="text/xml")
    
    # Add to conversation
    conversations[call_sid].append({"role": "user", "content": user_speech})
    
    # Get AI response
    ai_response = chat_with_gpt(conversations[call_sid])
    conversations[call_sid].append({"role": "assistant", "content": ai_response})
    
    print(f"AI replied: {ai_response}")
    
    # Clean for TTS
    clean_response = ai_response.replace('"', '').replace("'", "")
    if len(clean_response) > 150:
        clean_response = clean_response[:150]
    
    twiml = f"""<?xml version="1.0" encoding="UTF-8"?>
<Response>
    <Say voice="Polly.Aditi" language="hi-IN">{clean_response}</Say>
    <Gather input="speech" action="/process" method="POST" language="hi-IN,en-US" speechTimeout="5" timeout="10"/>
</Response>"""
    
    return Response(twiml, mimetype="text/xml")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8001, debug=True)