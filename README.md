# 🎭 Moodify - AI-Powered Emotion-Aware Voice Chatbot

![Moodify Banner](https://img.shields.io/badge/Moodify-Voice%20Chatbot-orange?style=for-the-badge)
![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.109+-green?style=for-the-badge&logo=fastapi)
![License](https://img.shields.io/badge/License-MIT-yellow?style=for-the-badge)

**Moodify** is a Dragon Ball Z themed voice chatbot that detects emotions from your voice and responds with mood-appropriate conversations. Talk to an AI that understands how you're feeling and adapts its responses accordingly!

## ✨ Features

🎤 **Voice Emotion Detection** - Detects 7 emotions from audio using state-of-the-art ML models
- Happy, Sad, Angry, Fear, Surprise, Disgust, Neutral

🤖 **AI-Powered Responses** - Generates contextual, emotion-aware replies using Groq's LLM

🎨 **Dragon Ball Z Theme** - Character transformations based on detected emotions
- Super Saiyan for Angry 😤
- Ultra Instinct for Happy 😊
- Base Form for Neutral 😐
- And more!

🔊 **Voice Activity Detection** - Automatically sends audio after 3 seconds of silence

💬 **Conversation Memory** - Maintains context across the conversation

😊 **Graceful Degradation** - Works with audio-only; face detection optional

## 🏗️ Architecture

```
┌─────────────┐      ┌──────────────┐      ┌─────────────┐
│   Frontend  │─────▶│   Backend    │─────▶│   Groq API  │
│  (React UI) │      │  (FastAPI)   │      │    (LLM)    │
└─────────────┘      └──────────────┘      └─────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │ HuggingFace  │
                     │ Audio Model  │
                     └──────────────┘
                            │
                            ▼
                     ┌──────────────┐
                     │  CNN Model   │
                     │  (Optional)  │
                     └──────────────┘
```

## 📁 Project Structure

```
moodify/
├── backend/                    # FastAPI backend
│   ├── app/
│   │   ├── api/               # API routes
│   │   ├── core/              # Core utilities
│   │   ├── models/            # ML models & schemas
│   │   ├── services/          # Business logic
│   │   ├── utils/             # Helper functions
│   │   └── main.py            # App entry point
│   ├── trained_models/        # CNN model (optional)
│   ├── requirements.txt
│   └── README.md
│
└── frontend/                  # React frontend
    ├── src/
    │   ├── components/        # UI components
    │   ├── services/          # API clients
    │   └── App.jsx
    ├── public/
    └── package.json
```

## 🚀 Quick Start

### Prerequisites

- **Python 3.10+**
- **Node.js 18+** (for frontend)
- **Groq API Key** ([Get one free](https://console.groq.com))
- **Optional:** Trained CNN model for face emotion detection

### Backend Setup

1. **Clone the repository**
```bash
git clone https://github.com/ShubrotoDas10/moodify.git
cd moodify/backend
```

2. **Create virtual environment**
```bash
python -m venv venv

# Activate on Windows
venv\Scripts\activate

# Activate on Mac/Linux
source venv/bin/activate
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

4. **Configure environment**
```bash
cp .env.example .env
```

Edit `.env` and add your Groq API key:
```env
GROQ_API_KEY=your_groq_api_key_here
```

5. **Run the backend**
```bash
python -m app.main
```

Backend will start on `http://localhost:8000`

### Frontend Setup

1. **Navigate to frontend**
```bash
cd ../frontend
```

2. **Install dependencies**
```bash
npm install
```

3. **Start development server**
```bash
npm run dev
```

Frontend will start on `http://localhost:5173`

## 🎯 Usage

1. **Open the app** in your browser (`http://localhost:5173`)
2. **Allow microphone access** when prompted
3. **Press the mic button** and start talking
4. **Stop talking** and wait 3 seconds - your message will auto-send
5. **Watch Goku transform** based on your emotion!
6. **See the AI response** tailored to your mood

## 📡 API Endpoints

### Main Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/chat/audio` | POST | Send audio, get emotion + response |
| `/chat/text` | POST | Text-only chat (fallback) |
| `/audio/detect-emotion` | POST | Audio emotion detection only |
| `/health/models` | GET | Check backend status |

### Example API Call

```bash
curl -X POST "http://localhost:8000/chat/audio" \
  -F "audio=@recording.wav"
```

**Response:**
```json
{
  "emotion": {
    "emotion": "happy",
    "confidence": 0.87,
    "probabilities": {...}
  },
  "chat_response": {
    "message": "That's wonderful! Keep that positive energy!",
    "emotion_detected": "happy"
  }
}
```

See full [API Documentation](./MOODIFY_API_DOCUMENTATION.md)

## 🛠️ Tech Stack

### Backend
- **FastAPI** - High-performance web framework
- **PyTorch** - ML model inference
- **HuggingFace Transformers** - Audio emotion detection
- **OpenCV** - Face detection (optional)
- **Groq API** - LLM for response generation
- **librosa** - Audio processing

### Frontend
- **React** - UI framework
- **Web Audio API** - Voice recording
- **Fetch API** - Backend communication
- **CSS3** - Dragon Ball Z themed styling

## 🎨 Emotion → Character Mapping

| Emotion | Character State |
|---------|----------------|
| 😤 Angry | Super Saiyan Goku (Golden aura) |
| 😊 Happy | Ultra Instinct Goku (Silver glow) |
| 😢 Sad | Base Goku (Looking down) |
| 😰 Fear | Injured Goku (Worried) |
| 😲 Surprise | Shocked Goku (Wide eyes) |
| 🤢 Disgust | Annoyed Vegeta (Scowling) |
| 😐 Neutral | Base Goku (Relaxed) |

## 🧪 Testing

### Test Backend Health
```bash
curl http://localhost:8000/health
```

### Test with Sample Audio
```bash
curl -X POST "http://localhost:8000/chat/audio" \
  -F "audio=@test_audio.wav"
```

### Run Unit Tests
```bash
cd backend
pytest
```

## 📦 Optional: CNN Face Emotion Detection

Moodify works great with audio-only, but you can add face emotion detection:

1. **Train or obtain a CNN model** for emotion recognition
2. **Place model file** in `backend/trained_models/cnn_face_emotion.pth`
3. **Restart backend** - it will automatically load the CNN

See [CNN_OPTIONAL.md](./backend/CNN_OPTIONAL.md) for details.

## 🐛 Troubleshooting

### Backend won't start
```bash
# Fix NumPy compatibility issue
pip install "numpy<2"
pip install opencv-python-headless==4.9.0.80
```

### Frontend can't connect
- Ensure backend is running on port 8000
- Check CORS settings in `.env`
- Try `http://localhost:8000/health` in browser

### Microphone not working
- Use HTTPS in production (required for mic access)
- Check browser permissions
- Ensure site is not blocked

### CNN model not loading
- This is OK! Backend works with audio-only
- Check logs for "⚠ CNN model not available"
- See [CNN_OPTIONAL.md](./backend/CNN_OPTIONAL.md)

## 📖 Documentation

- [Complete API Documentation](./MOODIFY_API_DOCUMENTATION.md)
- [CNN Optional Guide](./backend/CNN_OPTIONAL.md)
- [Frontend Development Guide](./LOVABLE_PROMPT.md)
- [Backend README](./backend/README.md)

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📝 Environment Variables

### Backend (.env)
```env
GROQ_API_KEY=your_groq_api_key          # Required
HF_TOKEN=your_hf_token                  # Optional
CNN_MODEL_PATH=./trained_models/cnn_face_emotion.pth  # Optional
AUDIO_CONFIDENCE_THRESHOLD=0.70
MAX_AUDIO_SIZE_MB=10
ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173
```

## 🎓 How It Works

1. **Voice Input** → User speaks into microphone
2. **VAD** → Frontend detects 3 seconds of silence
3. **Audio Sent** → WAV file sent to `/chat/audio` endpoint
4. **Emotion Detection** → HuggingFace model analyzes audio
5. **Response Generation** → Groq LLM creates mood-appropriate response
6. **Character Update** → Frontend displays matching DBZ character
7. **Chat Display** → Message shown with emotion badge

## 🔐 Security Notes

- Never commit `.env` files
- Use environment variables for API keys
- Enable CORS only for trusted origins
- Validate all file uploads
- Use HTTPS in production

## 📊 Performance

- **Emotion Detection:** ~1-2 seconds
- **Response Generation:** ~2-3 seconds
- **Total Response Time:** ~3-5 seconds
- **Supports:** Multiple concurrent users

## 🚀 Deployment

### Backend
- **Docker:** `docker-compose up -d`
- **Railway/Render:** Connect GitHub repo
- **AWS/GCP:** Use provided Dockerfile

### Frontend
- **Vercel:** `npm run build` → Deploy
- **Netlify:** Connect GitHub repo
- **Cloudflare Pages:** Auto-deploy on push

## 🌟 Future Enhancements

- [ ] Multi-language support
- [ ] Voice synthesis for AI responses
- [ ] Mobile app (React Native)
- [ ] Advanced emotion analytics
- [ ] Custom character themes
- [ ] Real-time conversation insights
- [ ] Group chat support

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Shubroto Das**
- GitHub: [@ShubrotoDas10](https://github.com/ShubrotoDas10)

## 🙏 Acknowledgments

- [Groq](https://groq.com) - For fast LLM inference
- [HuggingFace](https://huggingface.co) - For emotion detection models
- [Dragon Ball Z](https://dragonball.fandom.com) - For character inspiration
- [FastAPI](https://fastapi.tiangolo.com) - For the amazing framework

## ⭐ Star History

[![Star History Chart](https://api.star-history.com/svg?repos=ShubrotoDas10/moodify&type=Date)](https://star-history.com/#ShubrotoDas10/moodify&Date)

## 📞 Support

If you have questions or need help:
- Open an [Issue](https://github.com/ShubrotoDas10/moodify/issues)
- Check [Discussions](https://github.com/ShubrotoDas10/moodify/discussions)
- Read the [Documentation](./MOODIFY_API_DOCUMENTATION.md)

---

<div align="center">

**Made with ❤️ by Shubroto Das**

If you found this project helpful, please consider giving it a ⭐!

[Report Bug](https://github.com/ShubrotoDas10/moodify/issues) · [Request Feature](https://github.com/ShubrotoDas10/moodify/issues) · [Documentation](./MOODIFY_API_DOCUMENTATION.md)

</div>
