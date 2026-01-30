# Moodify Backend

Emotion-aware chatbot backend with audio and facial emotion detection using ML models and Groq API.

## Features

- 🎤 **Audio Emotion Detection** - Detect emotions from voice using HuggingFace models (Always Available)
- 😊 **Face Emotion Detection** - Detect emotions from facial expressions using CNN (Optional - can be added later)
- 🤖 **AI Chat Response** - Generate mood-appropriate responses using Groq API
- 🔄 **Emotion Fusion** - Combine audio and face emotions for higher accuracy (when CNN available)
- 📊 **Confidence Scoring** - Request confirmation when confidence is low
- 🚀 **Fast & Scalable** - Built with FastAPI for high performance
- ✨ **Graceful Degradation** - Works with audio-only if CNN model not available

## Architecture

```
Audio Input → Emotion Detection → Response Generation → User
Image Input → Face Detection → Emotion Analysis ↗
```

## Prerequisites

- Python 3.10+
- Groq API key (Required)
- HuggingFace token (Optional - only for gated models)
- Trained CNN model (Optional - can add later for face emotion detection)

**Note:** The backend works perfectly fine with just audio emotion detection. You can skip the CNN model for now and add it later when ready!

## Installation

### 1. Clone and Setup

```bash
git clone <your-repo>
cd moodify-backend
```

### 2. Create Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment

Copy `.env.example` to `.env` and fill in your credentials:

```bash
cp .env.example .env
```

Edit `.env`:
```env
GROQ_API_KEY=your_groq_api_key_here
HF_TOKEN=your_huggingface_token_here  # Optional
CNN_MODEL_PATH=./trained_models/cnn_face_emotion.pth
```

### 5. Add Your Trained Model (Optional)

**You can skip this step for now!** The backend works with audio-only emotion detection.

When you're ready to add face emotion detection, place your trained CNN model in the `trained_models/` directory:

```bash
cp /path/to/your/model.pth trained_models/cnn_face_emotion.pth
```

**IMPORTANT:** If adding CNN later, make sure the CNN architecture in `app/models/ml_models/cnn_architecture.py` matches your trained model!

### 6. Download HuggingFace Models (Optional)

```bash
python scripts/download_models.py
```

## Running the Application

### Development Mode

```bash
# Run with auto-reload
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or use the main file
python app/main.py
```

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Using Docker

```bash
# Build and run
docker-compose up --build

# Run in detached mode
docker-compose up -d

# Stop
docker-compose down
```

## API Endpoints

### Health Checks

- `GET /health` - Basic health check
- `GET /health/models` - Check if ML models are loaded
- `GET /health/ready` - Readiness check

### Emotion Detection

- `POST /audio/detect-emotion` - Detect emotion from audio only
- `POST /image/detect-emotion` - Detect emotion from face only

### Chat Endpoints

- `POST /chat/audio` - Chat with audio emotion detection
- `POST /chat/image` - Chat with face emotion detection
- `POST /chat/multimodal` - Chat with both audio and face
- `POST /chat/text` - Chat with text only

### API Documentation

- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Usage Examples

### Audio Chat Request

```bash
curl -X POST "http://localhost:8000/chat/audio" \
  -F "audio=@voice.wav" \
  -F "message=Hey, how are you?"
```

### Image Chat Request

```bash
curl -X POST "http://localhost:8000/chat/image" \
  -F "image=@face.jpg"
```

### Multimodal Request

```bash
curl -X POST "http://localhost:8000/chat/multimodal" \
  -F "audio=@voice.wav" \
  -F "image=@face.jpg" \
  -F "message=Optional text"
```

### Python Client Example

```python
import requests

# Audio emotion detection + chat
with open('audio.wav', 'rb') as audio_file:
    files = {'audio': audio_file}
    data = {'message': 'Hello!'}
    response = requests.post('http://localhost:8000/chat/audio', 
                           files=files, data=data)
    print(response.json())
```

## Project Structure

```
backend/
├── app/
│   ├── api/                    # API routes and middleware
│   ├── core/                   # Core utilities (logging, exceptions)
│   ├── models/                 # ML models and schemas
│   ├── services/               # Business logic services
│   ├── utils/                  # Helper utilities
│   ├── config.py              # Configuration
│   └── main.py                # FastAPI app
├── trained_models/            # Your CNN model goes here
├── storage/temp/              # Temporary file storage
├── scripts/                   # Utility scripts
├── tests/                     # Tests
├── requirements.txt           # Dependencies
├── Dockerfile                 # Docker configuration
└── README.md                  # This file
```

## Configuration

### Environment Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| `GROQ_API_KEY` | Groq API key | - | ✅ Yes |
| `HF_TOKEN` | HuggingFace token | - | ❌ No |
| `CNN_MODEL_PATH` | Path to CNN weights | `./trained_models/cnn_face_emotion.pth` | ❌ No (Optional) |
| `AUDIO_MODEL_NAME` | HF model for audio | `ehcalabres/wav2vec2-lg-xlsr-en-speech-emotion-recognition` | ✅ Yes |
| `AUDIO_CONFIDENCE_THRESHOLD` | Min confidence for audio | 0.70 | ❌ No |
| `FACE_CONFIDENCE_THRESHOLD` | Min confidence for face | 0.65 | ❌ No |
| `MAX_AUDIO_SIZE_MB` | Max audio file size | 10 | ❌ No |
| `MAX_IMAGE_SIZE_MB` | Max image file size | 5 | ❌ No |

### Emotion Strategies

The chatbot uses different strategies for different emotions:

- **Happy**: Enthusiastic, share jokes, maintain energy
- **Sad**: Empathetic, gentle humor, motivational content
- **Angry**: Calm, understanding, stress relief
- **Fear**: Reassuring, grounding exercises
- **Surprise**: Curious, engaging
- **Disgust**: Understanding, redirect focus
- **Neutral**: Friendly, conversational

## Customization

### Using Your Own CNN Model

1. Update the architecture in `app/models/ml_models/cnn_architecture.py` to match your model
2. Place your `.pth` file in `trained_models/`
3. Update `CNN_MODEL_PATH` in `.env`

### Changing Response Style

Edit emotion strategies in `app/core/constants.py`:

```python
EMOTION_STRATEGIES = {
    "happy": {
        "tone": "your custom tone",
        "goal": "your custom goal",
        "approach": "your custom approach"
    }
}
```

### Using Different LLM Models

Change the model in `app/services/groq_service.py`:

```python
self.model = "mixtral-8x7b-32768"  # or other Groq models
```

## Testing

Run tests:

```bash
# All tests
pytest

# Specific test file
pytest tests/test_audio_emotion.py

# With coverage
pytest --cov=app
```

## Troubleshooting

### Model Loading Issues

```bash
# Test model loading
python scripts/test_model_inference.py
```

### Audio Processing Errors

Make sure ffmpeg is installed:
```bash
# Ubuntu/Debian
sudo apt-get install ffmpeg

# macOS
brew install ffmpeg
```

### Face Detection Not Working

Ensure opencv-python is installed with:
```bash
pip install opencv-python
```

### Memory Issues

Reduce batch size or use smaller models, or increase server memory.

## Performance Optimization

- Use GPU if available (CUDA)
- Enable model caching
- Use worker processes for production
- Implement request queuing for high load

## Monitoring

Check logs for issues:
```bash
# In development
tail -f logs/moodify_*.log

# In Docker
docker-compose logs -f
```

## Security

- Never commit `.env` file
- Use environment variables for secrets
- Implement rate limiting in production
- Validate all file uploads
- Use HTTPS in production

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

[Your License Here]

## Support

For issues and questions:
- GitHub Issues: [your-repo]/issues
- Email: [your-email]

## Acknowledgments

- HuggingFace for audio emotion models
- Groq for LLM API
- FER2013 dataset for face emotion training
