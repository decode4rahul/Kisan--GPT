# 🌾 KisanGPT - Voice AI for Farmers

> **Empowering 600 Million Farmers with Zero Barriers** 🚀

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![OpenAI](https://img.shields.io/badge/OpenAI-GPT--4-orange.svg)](https://openai.com)
[![Twilio](https://img.shields.io/badge/Twilio-Voice-red.svg)](https://twilio.com)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## 🎯 What is KisanGPT?

KisanGPT is a **revolutionary voice-based AI agricultural expert** that helps farmers get instant expert advice through simple phone calls. No apps, no literacy barriers, no smartphones needed - just call **📞 04045210397** and speak in your native language!

## 🚨 The Problem We Solve

- 📱 **Basic Phones Only**: Most farmers own feature phones, not smartphones
- 📚 **Literacy Barriers**: Cannot read/write, need voice-based solutions  
- 🌐 **Language Gap**: Existing apps are English-only and text-based
- ⏰ **No Expert Access**: No timely help when crops are in danger

## ✨ Our Solution

### 🎙️ Voice-First AI Assistant
- **Zero Downloads** - Works on any phone
- **Zero Literacy** - Pure voice interaction
- **Zero Barriers** - Instant access to expertise

### 🗣️ How It Works
1. 📞 Farmer calls **04045210397**
2. 🤖 AI greets in their native language
3. 🗣️ Farmer describes problem naturally
4. 💡 AI provides expert advice with medicine prices

## 🌟 Features

### 🐛 Pest & Disease Diagnosis
```
"My cotton leaves are turning yellow and curling"
→ AI diagnoses + provides treatment with prices
```

### 💰 Real-Time Market Prices
```
"What's today's cotton price in Akola mandi?"
→ Live prices + selling recommendations
```

### 🌾 Crop Calendar Guidance
```
"When should I plant wheat?"
→ Season-specific, location-based advice
```

### 🌦️ Weather-Based Recommendations
```
"Should I spray pesticide today?"
→ Weather alerts + optimal timing
```

### 🧪 Fertilizer Timing
```
"My wheat is 45 days old, what should I apply?"
→ Customized recommendations + dealer info
```

### 📊 Harvest Optimization
```
"Are my tomatoes ready to pick?"
→ Best timing + market analysis
```

## 🛠️ Tech Stack

- **🐍 Backend**: Python + Flask
- **🧠 AI**: OpenAI GPT-4o-mini
- **📞 Voice**: Twilio Voice API
- **🗄️ Database**: Supabase
- **🌐 Frontend**: HTML/CSS/JavaScript
- **🔍 Price Data**: Web scraping APIs

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Twilio Account
- OpenAI API Key
- Supabase Account

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/yourusername/kisangpt.git
cd kisangpt
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Set up environment variables**
```bash
# Add your API keys to the respective files:
# - OpenAI API key in ai.py
# - Weather API key in ai.py  
# - Supabase credentials in db.py
```

4. **Run the application**
```bash
python call.py
```

5. **Start the frontend**
```bash
cd frontend
# Open index.html in your browser
```

## 📁 Project Structure

```
kisangpt/
├── 🤖 ai.py              # Core AI logic & conversation handling
├── 📞 call.py            # Flask app for Twilio voice integration
├── 🗄️ db.py              # Supabase database operations
├── 📋 requirements.txt   # Python dependencies
├── 🌐 frontend/          # Web interface
│   ├── index.html        # Main landing page
│   ├── style.css         # Styling
│   └── script.js         # JavaScript functionality
└── 📖 README.md          # This file
```

## 🎯 Core Components

### 🧠 AI Engine (`ai.py`)
- **Conversation Management**: Maintains context across calls
- **Multi-language Support**: Responds in farmer's native language
- **Weather Integration**: Real-time weather data for farming advice
- **Price Fetching**: Live medicine/fertilizer prices
- **Farmer Database**: Stores farmer profiles and chat history

### 📞 Voice Interface (`call.py`)
- **Twilio Integration**: Handles incoming voice calls
- **Speech-to-Text**: Converts farmer speech to text
- **Text-to-Speech**: Converts AI responses to voice
- **Session Management**: Tracks individual call sessions

### 🗄️ Database (`db.py`)
- **Farmer Profiles**: Name, location, language, phone number
- **Chat History**: Conversation logs for continuity
- **Supabase Integration**: Cloud database operations

## 🌍 Impact & Vision

### 📊 Target Reach
- **600M+ Indian Farmers** 🇮🇳
- **10+ Regional Languages** 🗣️
- **24/7 Expert Availability** ⏰
- **Zero Barriers to Access** 🚫

### 🎯 Use Cases
- 🐛 Crop disease identification & treatment
- 💰 Market price information & selling advice
- 🌱 Planting & harvesting guidance
- 🌦️ Weather-based farming decisions
- 🧪 Fertilizer & pesticide recommendations
- 📈 Yield optimization strategies

## 🤝 Contributing

We welcome contributions! Here's how you can help:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
4. 📤 Push to the branch (`git push origin feature/amazing-feature`)
5. 🔄 Open a Pull Request

## 📞 Contact & Support

### 🎯 Try KisanGPT Now!
**Call: 📞 04045210397**

### 📧 Get in Touch
- **Email**: contact@kisangpt.com
- **Location**: 📍 Gwalior, Madhya Pradesh, India

### 🐛 Report Issues
Found a bug? [Create an issue](https://github.com/yourusername/kisangpt/issues)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- 🌾 **Farmers** - The backbone of our nation
- 🤖 **OpenAI** - For powerful language models
- 📞 **Twilio** - For reliable voice infrastructure
- 🗄️ **Supabase** - For seamless database operations

---

<div align="center">

**🌾 Made with ❤️ for Indian Farmers 🇮🇳**

*Empowering agriculture through accessible AI technology*

[![Star this repo](https://img.shields.io/github/stars/yourusername/kisangpt?style=social)](https://github.com/yourusername/kisangpt)
[![Follow us](https://img.shields.io/twitter/follow/kisangpt?style=social)](https://twitter.com/kisangpt)

</div>