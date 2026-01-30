const API_BASE_URL = 'http://localhost:8000';

// Backend ke naye structure ke hisaab se interface
export interface EmotionResult {
  label: string; // Backend se 'label' aa raha hai
  confidence: number;
  needs_confirmation: boolean;
}

export interface ChatResponse {
  message: string; // AI ka motivating reply
  strategy: string; 
}

export interface AudioChatResponse {
  transcript: string; // Jo tumne bola (Whisper output)
  emotion: EmotionResult;
  chat_response: ChatResponse;
}

export interface HealthCheckResponse {
  status: string;
  models_loaded: boolean;
  audio_model: boolean;
  text_model: boolean;
}

export interface ConversationMessage {
  role: 'user' | 'assistant';
  content: string;
}

// Health check function
export async function checkBackendHealth(): Promise<HealthCheckResponse> {
  try {
    const response = await fetch(`${API_BASE_URL}/health/models`);
    if (!response.ok) throw new Error(`Health check failed: ${response.status}`);
    return await response.json();
  } catch (error) {
    console.error('Backend health check failed:', error);
    throw error;
  }
}

// MAIN FUNCTION: Audio processing ke liye
export async function sendAudioMessage(
  audioBlob: Blob
): Promise<AudioChatResponse> {
  const formData = new FormData();
  
  // File extension handle karna
  const extension = audioBlob.type.includes('webm') ? 'webm' : 
                    audioBlob.type.includes('mp4') ? 'm4a' : 'wav';
  
  formData.append('audio', audioBlob, `recording.${extension}`);

  try {
    // URL change ki hai taaki routes/audio.py se connect ho sake
    const response = await fetch(`${API_BASE_URL}/audio/detect-emotion`, {
      method: 'POST',
      body: formData,
    });

    if (!response.ok) {
      const errorText = await response.text();
      throw new Error(`Failed to process audio: ${response.status} - ${errorText}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Audio message failed:', error);
    throw error;
  }
}