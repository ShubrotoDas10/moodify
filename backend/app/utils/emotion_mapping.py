"""
Emotion mapping and strategy utilities
"""
from app.core.constants import EMOTION_STRATEGIES, AUDIO_EMOTION_LABELS
from typing import Dict


def normalize_emotion_label(emotion: str) -> str:
    """
    Normalize emotion labels from different sources
    
    Args:
        emotion: Raw emotion label
        
    Returns:
        Normalized emotion label
    """
    emotion = emotion.lower().strip()
    
    # Map audio model labels to standard labels
    if emotion in AUDIO_EMOTION_LABELS:
        return AUDIO_EMOTION_LABELS[emotion]
    
    return emotion


def get_emotion_strategy(emotion: str) -> Dict:
    """
    Get response strategy for a given emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        Strategy dictionary
    """
    normalized_emotion = normalize_emotion_label(emotion)
    
    # Return strategy or default to neutral
    return EMOTION_STRATEGIES.get(
        normalized_emotion, 
        EMOTION_STRATEGIES["neutral"]
    )


def combine_emotions(audio_emotion: str, face_emotion: str, 
                     audio_confidence: float, face_confidence: float) -> tuple:
    """
    Combine audio and face emotions to determine final emotion
    
    Args:
        audio_emotion: Emotion from audio
        face_emotion: Emotion from face
        audio_confidence: Audio confidence score
        face_confidence: Face confidence score
        
    Returns:
        Tuple of (final_emotion, final_confidence, method)
    """
    # Normalize emotions
    audio_emotion = normalize_emotion_label(audio_emotion)
    face_emotion = normalize_emotion_label(face_emotion)
    
    # If emotions match, high confidence
    if audio_emotion == face_emotion:
        combined_confidence = (audio_confidence + face_confidence) / 2
        return audio_emotion, combined_confidence, "agreement"
    
    # If confidence difference is large, trust the higher one
    confidence_diff = abs(audio_confidence - face_confidence)
    if confidence_diff > 0.3:
        if audio_confidence > face_confidence:
            return audio_emotion, audio_confidence, "audio_dominant"
        else:
            return face_emotion, face_confidence, "face_dominant"
    
    # If similar confidence but different emotions, weighted average
    # Slightly favor audio as it's often more reliable for emotion
    audio_weight = 0.6
    face_weight = 0.4
    
    if audio_confidence > face_confidence:
        return audio_emotion, audio_confidence * audio_weight + face_confidence * face_weight, "audio_weighted"
    else:
        return face_emotion, face_confidence * face_weight + audio_confidence * audio_weight, "face_weighted"


def map_response_tone(emotion: str) -> str:
    """
    Get appropriate tone for response based on emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        Tone description
    """
    strategy = get_emotion_strategy(emotion)
    return strategy.get("tone", "friendly and conversational")


def map_response_goal(emotion: str) -> str:
    """
    Get goal for response based on emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        Goal description
    """
    strategy = get_emotion_strategy(emotion)
    return strategy.get("goal", "create an engaging interaction")


def map_response_approach(emotion: str) -> str:
    """
    Get approach for response based on emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        Approach description
    """
    strategy = get_emotion_strategy(emotion)
    return strategy.get("approach", "be helpful and friendly")
