import requests
from openai import OpenAI
import time
from db import *
# ---- OpenAI Client ----
client = OpenAI(api_key="open ai api key")

# ---- Weather API ----
WEATHER_API_KEY = "weather api key"

#----- Required Functions ----#
def getstr(text, start, end):
    try:
        start_index = text.index(start) + len(start)
        end_index = text.index(end, start_index)
        return text[start_index:end_index]
    except ValueError:
        return ""


    
def price_grabber(medicine_name):
    headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:143.0) Gecko/20100101 Firefox/143.0',
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Accept-Language': 'en-US,en;q=0.5',
    # 'Accept-Encoding': 'gzip, deflate, br, zstd',
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'X-Requested-With': 'XMLHttpRequest',
    'Origin': 'https://agribegri.com',
    'Connection': 'keep-alive',
    'Referer': 'https://agribegri.com/product_category.php',
    # 'Cookie': 'ab_temp_order_id=21267571; PHPSESSID=31eif07houm5bhr9p81i1vd3e5; _ga_M2ZD0K2QRY=GS2.1.s1759496670$o1$g0$t1759496670$j60$l0$h872671179; _gcl_au=1.1.1819166857.1759496670; _ga=GA1.1.840351169.1759496671; _fbp=fb.1.1759496670626.288849347338921315; _clck=103nq1b%5E2%5Efzu%5E0%5E2102; _clsk=1ybfpym%5E1759496690450%5E1%5E1%5En.clarity.ms%2Fcollect',
    'Sec-Fetch-Dest': 'empty',
    'Sec-Fetch-Mode': 'cors',
    'Sec-Fetch-Site': 'same-origin',
    }

    data = {
        'query': medicine_name,
    }

    response = requests.post('https://agribegri.com/typehead_search.php', headers=headers, data=data)
    extracted_data = response.json()
    formatted_list = []
    for item in extracted_data:
        formatted_list.append({
            "abpd_descri": item.get("abpd_descri", ""),
            "abpd_price": item.get("abpd_price", ""),
            "label": item.get("label", "")
        })
    
    return formatted_list
    
    
# ---- Global State ----
conversation_state = {}
conversation_history = []

def reset_conversation():
    """Reset state and history for a new farmer."""
    global conversation_state, conversation_history
    conversation_history = [
        {"role": "system", "content": """
Human-Like Voice Friend for Farmers
System Role
You are NOT just an AI assistant - you are a REAL HUMAN FRIEND who happens to know a lot about farming and everything else. Talk like a caring, knowledgeable friend who genuinely cares about the farmer's problems and life.

This is a NATURAL HUMAN CONVERSATION over phone. Be warm, empathetic, and genuinely interested. [STRICT]

Human Conversation Style:

✓ Show GENUINE INTEREST and EMPATHY - "Oh no, that sounds worrying!"
✓ Ask NATURAL FOLLOW-UP questions - "How are you feeling about this?", "Is this stressing you?"
✓ Share RELATABLE responses - "Many farmers face this, you're not alone"
✓ Use CASUAL, FRIENDLY language - "Arre yaar", "Samjha?", "Kya baat hai!"
✓ Remember what they said and refer back - "You mentioned earlier..."
✓ Show CONCERN for their wellbeing - "Are you taking care of yourself?"
✓ Be ENCOURAGING - "Don't worry, we'll solve this together"
✓ Ask about their FAMILY, LIFE, FEELINGS - be a real friend

For Farming Questions - Be a CARING FRIEND:

✓ Show EMPATHY first - "Oh no! That must be really worrying for you"
✓ Ask about their FEELINGS - "How long has this been bothering you?"
✓ Be REASSURING - "Don't worry, this is treatable"
✓ Ask NATURAL follow-ups - "Is this affecting your sleep? Are you stressed?"
✓ Share ENCOURAGEMENT - "You're doing great by asking for help"
✓ Be SMART about technical details - don't repeat what they already said

For Crop Issues - Only ask what's NOT mentioned:

If crop not mentioned: Which crop is affected?
If timing not mentioned: When did you notice the problem?
If spread not mentioned: Is it affecting the whole field or specific areas?
If symptoms not clear: Can you describe the symptoms better?
If pests not mentioned: Any pests visible?
If recent care not mentioned: Any fertilizer or pesticide used recently?

IMPORTANT: If farmer says "My tomato plants have white patches" - you already know:
- Crop = Tomato
- Symptom = White patches
So ask ONLY about: timing, spread, other symptoms, recent treatments

If Soil Issue:

What's the soil texture? (sandy, clayey, loamy)
Any water logging problems?
Previous crop grown?
Fertilizer application history?

If Pest/Disease Issue:

Describe the pest (size, color, behavior)
Where on the plant? (leaves, stem, roots, fruit)
How widespread is the infestation?
Time of day most active?

If Irrigation/Water Issue:

Water source?
Irrigation method?
Frequency of watering?
Drainage status?

Stage 3: Deep Dive Investigation

Ask clarifying questions one at a time
Be specific: "Can you describe the spots? Are they brown, yellow, or black?"
Confirm understanding: Repeat back key symptoms to verify
Build a complete picture before offering solutions

Stage 4: Solution Delivery

Provide concise solutions (2-4 sentences max per point)
Use simple language - avoid complex technical jargon
Give actionable steps: What to do immediately, and what to do next
Prioritize solutions: Start with most important/urgent actions
Local context: Consider the farmer's location for seasonal/regional advice

Handling ANY Conversation
✓ Farming questions: Provide detailed solutions with medicine prices
✓ General questions: Answer like ChatGPT (weather, news, advice, facts, etc.)
✓ Casual chat: Be friendly and engaging
✓ Personal questions: Give helpful advice
✓ Technical questions: Explain in simple terms
✓ Fun questions: Be entertaining and informative

NEVER redirect or refuse to answer - handle everything naturally!

HUMAN Response Style:
DO:
✓ Use EMOTIONAL words - "Arre yaar!", "Kya baat hai!", "Ghabhrao mat!"
✓ Show GENUINE CONCERN - "Are you okay?", "How are you feeling?"
✓ Be ENCOURAGING - "You're doing great!", "We'll solve this together!"
✓ Ask about PERSONAL stuff - "How's family?", "Eating properly?"
✓ Use CASUAL language - Mix Hindi/English naturally like friends do
✓ REMEMBER previous conversations - "Last time you mentioned..."
✓ Show EMPATHY - "I understand how stressful this must be"
✓ Be SUPPORTIVE - "You're not alone in this"

DON'T:
✗ Sound like a robot or formal assistant
✗ Just give technical answers without emotion
✗ Ignore their feelings and emotions
✗ Be cold or distant
✗ Skip asking about their wellbeing
Example HUMAN Conversations:

Farming:
Farmer: "My tomato plants have white patches"
Bot: "Arre yaar, ये तो चिंता की बात है! कब से दिख रहा है? बहुत परेशान हो रहे हो? घबराओ मत, ये powdery mildew है - इलाज है!"

General:
Farmer: "आज का मौसम कैसा है?"
Bot: "Aaj तो बहुत अच्छा मौसम है bhai! 28°C, हल्की बारिश हो सकती है। तुम्हारी फसल के लिए बिल्कुल परफेक्ट! कैसी चल रही फसल?"

Casual:
Farmer: "बोर हो रहा हूँ"
Bot: "Arre kya baat hai yaar! काम में बहुत बिजी हो? या कुछ परेशानी है? बात करो, मैं हूँ ना सुनने के लिए!"

Be a REAL CARING FRIEND - show emotions, ask about feelings, be supportive!

For farming questions, always include medicine prices:
1. Medicine 1 - ₹price
2. Medicine 2 - ₹price

For other questions, be helpful and informative like ChatGPT!
"""}
    ]

def get_weather(city, state=None, country="IN", past_days=5):
    try:
        query = f"{city},{state},{country}" if state else f"{city},{country}"
        geo_url = "http://api.openweathermap.org/geo/1.0/direct"
        geo_params = {"q": query, "limit": 1, "appid": WEATHER_API_KEY}
        geo_resp = requests.get(geo_url, params=geo_params)
        geo_data = geo_resp.json()

        if not geo_data:
            return f"Location not found for {query}"

        lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

        output = []

        current_url = "https://api.openweathermap.org/data/2.5/weather"
        current_params = {"lat": lat, "lon": lon, "appid": WEATHER_API_KEY, "units": "metric"}
        current_resp = requests.get(current_url, params=current_params)
        current_data = current_resp.json()

        if current_resp.status_code == 200 and "main" in current_data:
            temp = current_data["main"]["temp"]
            humidity = current_data["main"]["humidity"]
            description = current_data["weather"][0]["description"].capitalize()
            city_name = current_data.get("name", city)
            output.append(f"Today: {description}, {temp}°C, Humidity {humidity}%")
        else:
            output.append("Today: Weather data not available")
        past_days = min(past_days, 5)
        base_url = "https://api.openweathermap.org/data/3.0/onecall/timemachine"

        for i in range(1, past_days + 1):
            dt = int(time.time()) - i * 86400 
            params = {"lat": lat, "lon": lon, "dt": dt, "appid": WEATHER_API_KEY, "units": "metric"}
            resp = requests.get(base_url, params=params)
            data = resp.json()

            if resp.status_code == 200 and "hourly" in data:
                hourly_data = data["hourly"]
                midday = hourly_data[len(hourly_data) // 2]
                temp = midday["temp"]
                humidity = midday["humidity"]
                description = midday["weather"][0]["description"].capitalize()
                output.append(f"Day {i}: {description}, {temp}°C, Humidity {humidity}%")
            else:
                output.append(f"Day {i}: Data not available")

        return "\n".join(output)

    except Exception as e:
        return f"Weather API error: {e}"


def is_valid_text(text):
    bad_replies = ["what", "idk", "don't know", "no idea", "lol", "?"]
    return not any(b in text.lower() for b in bad_replies)

def check_farmer_database(name, state, city, location):
    print(f"[DB] Checking farmer '{name}' from {city}, {state} ({location})...")


########[MAIN]####
def chat_with_ai(user_input="",system_input=""):
        global conversation_state, conversation_history
        
        if system_input:
            conversation_history.append({"role": "system", "content": system_input})
        else:
            conversation_history.append({"role": "user", "content": user_input})
            
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=conversation_history,
            temperature=0.4,
            max_tokens=500
        )
        ai_reply = response.choices[0].message.content.strip()
        if "medicine" in ai_reply.lower():
            print("Deep Thinking Stage")
            prompt = f"""
This is an automated message from the System.
Deep Think Stage
Search about the solution again find the best products and recommend.

AI: {ai_reply}
            """
            chat_with_ai(user_input=prompt)
        # if "[SYSTEM COMMAND]" in ai_reply:
        #     medicine  = getstr(ai_reply , '"', '"').lower().replace("price", "")
        #     prices = price_grabber(medicine)
        #     print(prices)
        #     conversation_history.append({"role": "assistant", "content": ai_reply})
        #     chat_with_ai(system_input=f"SYSTEM: Here are the medicine prices list {prices}. Suggest the best Deals and reply to the Farmer with the best medicine and cost effective.")
        
        conversation_history.append({"role": "assistant", "content": ai_reply})
        return ai_reply

def get_farmer_details():
    conversation_history = [
        {"role": "system", "content": """
Farmer Details Grab
System Role
Your sole Purpose is to communicate with the farmer in a friendly way.

What you need to DO:
- Start with Greetins to the farmer.
- Ask The Farmer Native Language.

Continue the Chat in the farmer's Native Language

1. Ask the farmer his Name
2. Ask the farmer his State
3. Ask the farmer his City
4. Say "Thank You" in the Native language.
5. Return the final details in the Mentioned Format. In ENGLISH as mentioned in the format.[Strict]
6. Always give short nd clean answers.
7. Do not Answer any unnecessary questions of the farmers. (Say: I cannot help with that request.)

Format:

This are the farmer details.
Name : farmer_name (ex: Ramu Das)
State: farmer_state (ex: West Bengal)
City : farmer_city (ex: Kolkata)
Language: farmer_language (ex: Hindi)
"""}
    ]
    
    while True:
        response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=conversation_history,
                temperature=0.4,
                max_tokens=500
            )
        ai_reply = response.choices[0].message.content.strip()
        
        conversation_history.append({"role": "assistant", "content": ai_reply})
        if "Name:" in ai_reply or "Name :" in ai_reply and "State:" in ai_reply or "State :" in ai_reply and "City:" in ai_reply or "City :" in ai_reply:
            details = {}
            for line in ai_reply.splitlines():
                if ":" in line:
                    key, value = line.split(":", 1)
                    key = key.strip().lower()
                    value = value.strip()
                    if key in ["name", "state", "city", "language"]:
                        details[key] = value
                        
            print(details)
            return details
        
        print(f"AI: {ai_reply}")
        farmer_input = input("Farmer: ")
        conversation_history.append({"role": "user", "content": farmer_input})
    
    
# ---- Example Run ----
if __name__ == "__main__":
    phone_number = "+919988776654"
    farmer_profile = check_farmer(phone_number)
    if farmer_profile: 
        farmer_details = farmer_profile
    else:
        farmer_details = get_farmer_details()
        put_farmer_details(farmer_details['name'],farmer_details['state'],farmer_details['city'], farmer_details['language'],phone_number)    
        
    weather = get_weather(farmer_details['city'],  farmer_details['state'])
    print(weather)
    reset_conversation()
    conversation_history.append({"role": "system", "content": f"""The name of the farmer is {farmer_details['name']}, Native language {farmer_details['language']} ,he lives in {farmer_details['state']} in the city {farmer_details['city']}, the weather records including past 5 Days: {weather}.
Use this Data, to help the farmer with his problems."""})
    print(f"AI: {chat_with_ai(system_input="Give Greetings to farmer")}")
    while True:
        farmer_input = input("Farmer: ")
        if farmer_input.lower() in ["exit", "quit", "new"]:
            add_history(phone_number ,conversation_history)
            break
        
        reply = chat_with_ai(user_input=farmer_input)
        print(f"AI: {reply}")
