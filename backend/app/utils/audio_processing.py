"""
Audio processing utilities
"""
import librosa
import soundfile as sf
import numpy as np
from pathlib import Path
from pydub import AudioSegment
from app.core.logging_config import log
from app.core.exceptions import AudioProcessingError
from app.core.constants import AUDIO_SAMPLE_RATE


def convert_to_wav(input_path: str, output_path: str = None) -> str:
    """
    Convert audio file to WAV format
    
    Args:
        input_path: Path to input audio file
        output_path: Path for output WAV file (optional)
        
    Returns:
        Path to converted WAV file
    """
    try:
        input_path = Path(input_path)
        
        if output_path is None:
            output_path = input_path.with_suffix('.wav')
        
        # If already WAV, just return the path
        if input_path.suffix.lower() == '.wav':
            return str(input_path)
        
        log.info(f"Converting {input_path.suffix} to WAV")
        
        # Load audio with pydub
        audio = AudioSegment.from_file(str(input_path))
        
        # Export as WAV
        audio.export(str(output_path), format='wav')
        
        log.info(f"Converted audio saved to: {output_path}")
        return str(output_path)
        
    except Exception as e:
        log.error(f"Audio conversion failed: {str(e)}")
        raise AudioProcessingError(f"Failed to convert audio: {str(e)}")


def resample_audio(audio_path: str, target_sr: int = AUDIO_SAMPLE_RATE) -> tuple:
    """
    Load and resample audio to target sample rate
    
    Args:
        audio_path: Path to audio file
        target_sr: Target sample rate (default 16000 Hz)
        
    Returns:
        Tuple of (audio_data, sample_rate)
    """
    try:
        log.info(f"Loading audio: {audio_path}")
        
        # Load audio
        audio_data, sr = librosa.load(audio_path, sr=target_sr, mono=True)
        
        log.info(f"Audio loaded: {len(audio_data)} samples at {sr} Hz")
        return audio_data, sr
        
    except Exception as e:
        log.error(f"Audio loading failed: {str(e)}")
        raise AudioProcessingError(f"Failed to load audio: {str(e)}")


def get_audio_duration(audio_path: str) -> float:
    """
    Get audio duration in seconds
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Duration in seconds
    """
    try:
        audio_data, sr = librosa.load(audio_path, sr=None)
        duration = len(audio_data) / sr
        return duration
    except Exception as e:
        log.error(f"Failed to get audio duration: {str(e)}")
        return 0.0


def extract_audio_features(audio_data: np.ndarray, sr: int) -> dict:
    """
    Extract features from audio (optional - for future use)
    
    Args:
        audio_data: Audio samples
        sr: Sample rate
        
    Returns:
        Dictionary of audio features
    """
    try:
        features = {}
        
        # MFCCs
        mfccs = librosa.feature.mfcc(y=audio_data, sr=sr, n_mfcc=13)
        features['mfccs'] = mfccs
        
        # Zero crossing rate
        zcr = librosa.feature.zero_crossing_rate(audio_data)
        features['zcr'] = zcr
        
        # Spectral centroid
        spectral_centroids = librosa.feature.spectral_centroid(y=audio_data, sr=sr)
        features['spectral_centroid'] = spectral_centroids
        
        # RMS energy
        rms = librosa.feature.rms(y=audio_data)
        features['rms'] = rms
        
        return features
        
    except Exception as e:
        log.error(f"Feature extraction failed: {str(e)}")
        return {}


def preprocess_audio_for_model(audio_path: str) -> str:
    """
    Preprocess audio file for emotion detection model
    
    Args:
        audio_path: Path to audio file
        
    Returns:
        Path to preprocessed audio file
    """
    try:
        # Convert to WAV if needed
        wav_path = convert_to_wav(audio_path)
        
        # Resample to target sample rate
        audio_data, sr = resample_audio(wav_path, AUDIO_SAMPLE_RATE)
        
        # Save preprocessed audio
        output_path = Path(wav_path).with_stem(f"{Path(wav_path).stem}_processed")
        sf.write(str(output_path), audio_data, sr)
        
        log.info(f"Preprocessed audio saved: {output_path}")
        return str(output_path)
        
    except Exception as e:
        log.error(f"Audio preprocessing failed: {str(e)}")
        raise AudioProcessingError(f"Failed to preprocess audio: {str(e)}")
