# Moodify Backend - Quick Start Guide

Get your Moodify backend running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.10+ installed
- [ ] Groq API key ([Get one here](https://console.groq.com))
- [ ] Git installed
- [ ] Your trained CNN model (`.pth` file) - **OPTIONAL! Can skip for now**

## Step-by-Step Setup

### 1. Clone & Navigate (30 seconds)

```bash
cd moodify-backend
```

### 2. Create Virtual Environment (1 minute)

```bash
python -m venv venv

# Activate it
# On macOS/Linux:
source venv/bin/activate

# On Windows:
venv\Scripts\activate
```

### 3. Install Dependencies (2 minutes)

```bash
pip install -r requirements.txt
```

### 4. Configure Environment (1 minute)

```bash
# Copy example env file
cp .env.example .env

# Edit .env with your favorite editor
nano .env  # or vim, code, etc.
```

Add your Groq API key:
```env
GROQ_API_KEY=gsk_your_actual_key_here
```

### 5. Add Your Model (Optional - Can Skip!)

**You can skip this step!** The backend works perfectly with just audio emotion detection.

If you want face emotion detection too:
```bash
# Copy your trained CNN model
cp /path/to/your/trained_model.pth trained_models/cnn_face_emotion.pth
```

**Note:** You can always add this later. The backend will work fine without it!

### 6. Run the Server! (10 seconds)

```bash
python app/main.py
```

You should see:
```
INFO:     Started server process
INFO:     Waiting for application startup.
INFO:     Loading ML models...
INFO:     Loading audio emotion model...
INFO:     ✓ Audio emotion model loaded successfully
INFO:     Loading CNN face emotion model...
INFO:     ⚠ CNN model not available - face emotion detection disabled
INFO:     Model loading complete - Audio emotion detection ready!
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Don't worry about the CNN warning!** Your audio chatbot is fully functional.

### 7. Test It! (30 seconds)

Open your browser to `http://localhost:8000/docs`

You'll see the interactive API documentation!

Try the health check:
```bash
curl http://localhost:8000/health
```

## Quick Test with curl

### Test Audio Emotion Detection

```bash
curl -X POST "http://localhost:8000/chat/audio" \
  -F "audio=@your_audio.wav" \
  -F "message=Hello!"
```

### Test Face Emotion Detection

```bash
curl -X POST "http://localhost:8000/chat/image" \
  -F "image=@your_face.jpg"
```

## Troubleshooting

### "Module not found" errors
```bash
# Make sure you're in the venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Model file not found"
```bash
# This is OK! CNN is optional. Check the logs:
# If it says "Audio emotion model loaded successfully", you're good!

# Only if you want face detection:
ls trained_models/cnn_face_emotion.pth
```

### "Groq API error"
```bash
# Check your .env file
cat .env | grep GROQ_API_KEY
```

### Audio processing errors
```bash
# Install ffmpeg
# Ubuntu/Debian:
sudo apt-get install ffmpeg

# macOS:
brew install ffmpeg

# Windows:
# Download from https://ffmpeg.org/download.html
```

## Next Steps

1. **Frontend Integration**: Connect your React/Vue/etc. frontend
2. **Test with real data**: Record some audio and take photos
3. **Customize responses**: Edit `app/core/constants.py` emotion strategies
4. **Deploy**: Use Docker or deploy to cloud platform

## Common Commands

```bash
# Start development server with auto-reload
uvicorn app.main:app --reload

# Run tests
pytest

# Clean up temp files
python scripts/cleanup_temp_files.py

# Download HF models (if needed)
python scripts/download_models.py

# Test model loading
python scripts/test_model_inference.py
```

## API Endpoints

- `GET /` - Welcome message
- `GET /docs` - Interactive API docs
- `GET /health` - Health check
- `POST /chat/audio` - Audio emotion + chat
- `POST /chat/image` - Face emotion + chat
- `POST /chat/multimodal` - Both audio + face
- `POST /chat/text` - Text only chat

## Environment Variables Reference

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `GROQ_API_KEY` | ✅ Yes | - | Your Groq API key |
| `HF_TOKEN` | ❌ No | - | HuggingFace token (for gated models) |
| `CNN_MODEL_PATH` | ❌ No (Optional) | `./trained_models/cnn_face_emotion.pth` | Path to CNN model - not needed for audio-only |
| `DEBUG` | ❌ No | `True` | Debug mode |
| `LOG_LEVEL` | ❌ No | `INFO` | Logging level |

## Production Deployment

### Using Docker

```bash
# Build image
docker build -t moodify-backend .

# Run container
docker run -p 8000:8000 --env-file .env moodify-backend

# Or use docker-compose
docker-compose up -d
```

### Using systemd (Linux)

Create `/etc/systemd/system/moodify.service`:

```ini
[Unit]
Description=Moodify Backend
After=network.target

[Service]
Type=simple
User=your-user
WorkingDirectory=/path/to/moodify-backend
Environment="PATH=/path/to/venv/bin"
ExecStart=/path/to/venv/bin/uvicorn app.main:app --host 0.0.0.0 --port 8000
Restart=always

[Install]
WantedBy=multi-user.target
```

Then:
```bash
sudo systemctl enable moodify
sudo systemctl start moodify
```

## Need Help?

- Check the full [README.md](README.md)
- Review API docs at `/docs` endpoint
- Check logs for error messages
- Verify all dependencies are installed
- Ensure your CNN model architecture matches

## Success! 🎉

Your Moodify backend is now running! Time to build an amazing frontend or test with API calls.

Happy coding! 😊
