"""
Application-wide constants
"""

# Emotion labels (adjust based on your CNN model's classes)
EMOTION_LABELS = [
    "angry",
    "disgust",
    "fear",
    "happy",
    "sad",
    "surprise",
    "neutral"
]

# Audio emotion labels (from HuggingFace model)
AUDIO_EMOTION_LABELS = {
    "angry": "angry",
    "calm": "neutral",
    "disgust": "disgust",
    "fearful": "fear",
    "happy": "happy",
    "neutral": "neutral",
    "sad": "sad",
    "surprised": "surprise"
}

# Emotion to response strategy mapping
EMOTION_STRATEGIES = {
    "happy": {
        "tone": "enthusiastic and cheerful",
        "goal": "maintain and amplify their positive mood",
        "approach": "share jokes, celebrate with them, keep the energy high"
    },
    "sad": {
        "tone": "empathetic and gentle",
        "goal": "provide comfort and emotional support",
        "approach": "listen actively, offer gentle humor, share motivational content"
    },
    "angry": {
        "tone": "calm and understanding",
        "goal": "help them process their feelings and find calm",
        "approach": "validate their emotions, suggest calming techniques, provide stress relief"
    },
    "fear": {
        "tone": "reassuring and supportive",
        "goal": "provide reassurance and safety",
        "approach": "offer grounding exercises, share comforting words, be a steady presence"
    },
    "surprise": {
        "tone": "curious and engaging",
        "goal": "engage with their excitement or curiosity",
        "approach": "share interesting facts, ask exploratory questions"
    },
    "disgust": {
        "tone": "understanding and redirecting",
        "goal": "acknowledge their feelings and shift focus",
        "approach": "validate their reaction, gently redirect to more positive topics"
    },
    "neutral": {
        "tone": "friendly and conversational",
        "goal": "create an engaging and pleasant interaction",
        "approach": "light humor, interesting conversation, explore their interests"
    }
}

# Response length targets
RESPONSE_LENGTH = {
    "short": 50,
    "medium": 100,
    "long": 200
}

# File processing
AUDIO_SAMPLE_RATE = 16000
IMAGE_SIZE = (48, 48)  # For CNN input
FACE_CASCADE_PATH = "haarcascade_frontalface_default.xml"
