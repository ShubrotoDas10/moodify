"""
Custom exception classes for Moodify
"""


class MoodifyException(Exception):
    """Base exception for Moodify application"""
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)


class ModelLoadError(MoodifyException):
    """Exception raised when model fails to load"""
    def __init__(self, message: str = "Failed to load ML model"):
        super().__init__(message, status_code=500)


class AudioProcessingError(MoodifyException):
    """Exception raised during audio processing"""
    def __init__(self, message: str = "Audio processing failed"):
        super().__init__(message, status_code=400)


class ImageProcessingError(MoodifyException):
    """Exception raised during image processing"""
    def __init__(self, message: str = "Image processing failed"):
        super().__init__(message, status_code=400)


class EmotionDetectionError(MoodifyException):
    """Exception raised during emotion detection"""
    def __init__(self, message: str = "Emotion detection failed"):
        super().__init__(message, status_code=500)


class GroqAPIError(MoodifyException):
    """Exception raised when Groq API call fails"""
    def __init__(self, message: str = "Groq API call failed"):
        super().__init__(message, status_code=502)


class FileValidationError(MoodifyException):
    """Exception raised when file validation fails"""
    def __init__(self, message: str = "File validation failed"):
        super().__init__(message, status_code=400)


class LowConfidenceError(MoodifyException):
    """Exception raised when emotion confidence is too low"""
    def __init__(self, message: str = "Low confidence in emotion detection", confidence: float = 0.0):
        self.confidence = confidence
        super().__init__(message, status_code=200)  # Not really an error, more of a signal
