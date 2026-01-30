"""
Prompt templates for Groq API responses
"""
from app.utils.emotion_mapping import get_emotion_strategy


def create_system_prompt(emotion: str) -> str:
    """
    Create system prompt based on detected emotion
    
    Args:
        emotion: Detected emotion
        
    Returns:
        System prompt string
    """
    strategy = get_emotion_strategy(emotion)
    
    system_prompt = f"""You are Moodify, an empathetic AI companion designed to improve people's moods through conversation.

The user is currently feeling: {emotion}

Your approach:
- Tone: {strategy['tone']}
- Goal: {strategy['goal']}
- Method: {strategy['approach']}

Guidelines:
1. Keep responses conversational, warm, and natural (2-4 sentences typically)
2. Match the emotional context - don't be overly cheerful with someone who's sad
3. Use appropriate humor when suitable, but be sensitive to the user's state
4. Be genuine and avoid clichés or generic responses
5. If the user seems to need professional help, gently suggest it
6. Don't mention that you detected their emotion unless they ask
7. Focus on being helpful and uplifting in a natural way

Remember: You're here to be a supportive presence, not to solve all their problems."""
    
    return system_prompt


def create_user_prompt(user_message: str = None, emotion: str = None) -> str:
    """
    Create user prompt
    
    Args:
        user_message: Optional user message
        emotion: Detected emotion context
        
    Returns:
        User prompt string
    """
    if user_message:
        return user_message
    
    # If no message, generate opening based on emotion
    if emotion:
        openings = {
            "happy": "Hey! I'm feeling pretty good right now!",
            "sad": "I'm not feeling great today...",
            "angry": "I'm really frustrated right now.",
            "fear": "I'm feeling a bit anxious...",
            "surprise": "Wow, something unexpected just happened!",
            "disgust": "Ugh, I'm not happy about something...",
            "neutral": "Hey there!"
        }
        return openings.get(emotion, "Hello!")
    
    return "Hello!"


def create_conversation_context(emotion: str, previous_messages: list = None) -> str:
    """
    Create conversation context for Groq
    
    Args:
        emotion: Current detected emotion
        previous_messages: Previous conversation messages
        
    Returns:
        Context string
    """
    context_parts = [f"Current emotion: {emotion}"]
    
    if previous_messages and len(previous_messages) > 0:
        context_parts.append("\nPrevious conversation:")
        for msg in previous_messages[-3:]:  # Last 3 messages
            role = msg.get('role', 'user')
            content = msg.get('content', '')
            context_parts.append(f"{role}: {content}")
    
    return "\n".join(context_parts)


# Emotion-specific response starters (for variety)
RESPONSE_STARTERS = {
    "happy": [
        "That's wonderful to hear!",
        "I love your energy!",
        "Keep that positive vibe going!",
        "That's fantastic!",
    ],
    "sad": [
        "I hear you, and I'm here for you.",
        "That sounds really tough.",
        "I'm sorry you're going through this.",
        "It's okay to feel this way.",
    ],
    "angry": [
        "I can understand why you'd feel that way.",
        "That does sound frustrating.",
        "It's valid to feel angry about that.",
        "Let's talk through this.",
    ],
    "fear": [
        "It's okay, I'm here with you.",
        "Those feelings are completely valid.",
        "Let's take this one step at a time.",
        "You're not alone in feeling this way.",
    ],
    "surprise": [
        "Wow, that's quite something!",
        "I can imagine that caught you off guard!",
        "That must have been unexpected!",
        "What a moment!",
    ],
    "disgust": [
        "I understand that reaction.",
        "That doesn't sound pleasant.",
        "I get why you'd feel that way.",
        "Fair enough.",
    ],
    "neutral": [
        "Hey there!",
        "What's on your mind?",
        "How can I help brighten your day?",
        "I'm here to chat!",
    ]
}


def get_response_starter(emotion: str, index: int = 0) -> str:
    """
    Get a response starter for the emotion
    
    Args:
        emotion: Detected emotion
        index: Index of starter to use (for variety)
        
    Returns:
        Response starter string
    """
    starters = RESPONSE_STARTERS.get(emotion, RESPONSE_STARTERS["neutral"])
    return starters[index % len(starters)]
