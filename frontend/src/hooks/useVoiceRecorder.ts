import { useState, useRef, useCallback, useEffect } from 'react';

interface UseVoiceRecorderOptions {
  silenceDuration?: number;
  silenceThreshold?: number;
  onAutoSend?: (audioBlob: Blob) => void;
  onVolumeChange?: (volume: number) => void;
  onCountdownChange?: (seconds: number | null) => void;
}

interface UseVoiceRecorderReturn {
  isRecording: boolean;
  isPaused: boolean;
  volume: number;
  countdown: number | null;
  frequencyData: Uint8Array | null;
  startRecording: () => Promise<void>;
  stopRecording: () => Promise<Blob | null>;
  cancelRecording: () => void;
}

export function useVoiceRecorder({
  silenceDuration = 3000,
  silenceThreshold = 0.02,
  onAutoSend,
  onVolumeChange,
  onCountdownChange,
}: UseVoiceRecorderOptions = {}): UseVoiceRecorderReturn {
  const [isRecording, setIsRecording] = useState(false);
  const [isPaused, setIsPaused] = useState(false);
  const [volume, setVolume] = useState(0);
  const [countdown, setCountdown] = useState<number | null>(null);
  const [frequencyData, setFrequencyData] = useState<Uint8Array | null>(null);

  const mediaRecorderRef = useRef<MediaRecorder | null>(null);
  const audioContextRef = useRef<AudioContext | null>(null);
  const analyzerRef = useRef<AnalyserNode | null>(null);
  const streamRef = useRef<MediaStream | null>(null);
  const chunksRef = useRef<Blob[]>([]);
  const silenceTimerRef = useRef<NodeJS.Timeout | null>(null);
  const countdownIntervalRef = useRef<NodeJS.Timeout | null>(null);
  const animationFrameRef = useRef<number | null>(null);
  const lastSpeakTimeRef = useRef<number>(0);

  const clearTimers = useCallback(() => {
    if (silenceTimerRef.current) {
      clearTimeout(silenceTimerRef.current);
      silenceTimerRef.current = null;
    }
    if (countdownIntervalRef.current) {
      clearInterval(countdownIntervalRef.current);
      countdownIntervalRef.current = null;
    }
    if (animationFrameRef.current) {
      cancelAnimationFrame(animationFrameRef.current);
      animationFrameRef.current = null;
    }
    setCountdown(null);
    onCountdownChange?.(null);
  }, [onCountdownChange]);

  const stopMediaStream = useCallback(() => {
    if (streamRef.current) {
      streamRef.current.getTracks().forEach(track => track.stop());
      streamRef.current = null;
    }
    if (audioContextRef.current && audioContextRef.current.state !== 'closed') {
      audioContextRef.current.close();
      audioContextRef.current = null;
    }
    analyzerRef.current = null;
  }, []);

  const startCountdown = useCallback(() => {
    let seconds = 3;
    setCountdown(seconds);
    onCountdownChange?.(seconds);

    countdownIntervalRef.current = setInterval(() => {
      seconds -= 1;
      setCountdown(seconds);
      onCountdownChange?.(seconds);

      if (seconds <= 0) {
        clearInterval(countdownIntervalRef.current!);
        countdownIntervalRef.current = null;
      }
    }, 1000);
  }, [onCountdownChange]);

  const monitorAudio = useCallback(() => {
    if (!analyzerRef.current || !isRecording) return;

    const analyzer = analyzerRef.current;
    const bufferLength = analyzer.fftSize;
    const dataArray = new Uint8Array(bufferLength);
    const frequencyArray = new Uint8Array(analyzer.frequencyBinCount);

    const checkVolume = () => {
      if (!isRecording || !analyzerRef.current) return;

      analyzer.getByteTimeDomainData(dataArray);
      analyzer.getByteFrequencyData(frequencyArray);

      // Calculate volume (RMS)
      let sum = 0;
      for (let i = 0; i < bufferLength; i++) {
        const v = (dataArray[i] - 128) / 128;
        sum += v * v;
      }
      const rms = Math.sqrt(sum / bufferLength);
      setVolume(rms);
      onVolumeChange?.(rms);

      // Update frequency data for visualization
      setFrequencyData(new Uint8Array(frequencyArray));

      // Check if user is speaking
      if (rms > silenceThreshold) {
        // User is speaking - reset silence detection
        lastSpeakTimeRef.current = Date.now();
        
        if (silenceTimerRef.current) {
          clearTimers();
        }
      } else if (chunksRef.current.length > 0 && !silenceTimerRef.current) {
        // User stopped speaking - start silence timer
        const timeSinceLastSpeak = Date.now() - lastSpeakTimeRef.current;
        
        if (timeSinceLastSpeak > 500) {
          // Start countdown
          startCountdown();
          
          silenceTimerRef.current = setTimeout(async () => {
            // Auto-stop and send
            const blob = await stopRecording();
            if (blob && onAutoSend) {
              onAutoSend(blob);
            }
          }, silenceDuration);
        }
      }

      animationFrameRef.current = requestAnimationFrame(checkVolume);
    };

    animationFrameRef.current = requestAnimationFrame(checkVolume);
  }, [isRecording, silenceThreshold, silenceDuration, onAutoSend, onVolumeChange, clearTimers, startCountdown]);

  const startRecording = useCallback(async () => {
    try {
      const stream = await navigator.mediaDevices.getUserMedia({ 
        audio: {
          echoCancellation: true,
          noiseSuppression: true,
          autoGainControl: true,
        } 
      });
      
      streamRef.current = stream;

      // Setup audio analysis
      const audioContext = new AudioContext();
      audioContextRef.current = audioContext;
      
      const source = audioContext.createMediaStreamSource(stream);
      const analyzer = audioContext.createAnalyser();
      analyzer.fftSize = 2048;
      analyzer.smoothingTimeConstant = 0.8;
      source.connect(analyzer);
      analyzerRef.current = analyzer;

      // Setup media recorder
      const mediaRecorder = new MediaRecorder(stream, {
        mimeType: MediaRecorder.isTypeSupported('audio/webm') ? 'audio/webm' : 'audio/mp4',
      });
      
      mediaRecorderRef.current = mediaRecorder;
      chunksRef.current = [];

      mediaRecorder.ondataavailable = (e) => {
        if (e.data.size > 0) {
          chunksRef.current.push(e.data);
        }
      };

      mediaRecorder.start(100); // Collect data every 100ms
      setIsRecording(true);
      setIsPaused(false);
      lastSpeakTimeRef.current = Date.now();

    } catch (error) {
      console.error('Failed to start recording:', error);
      throw error;
    }
  }, []);

  const stopRecording = useCallback(async (): Promise<Blob | null> => {
    return new Promise((resolve) => {
      if (!mediaRecorderRef.current || !isRecording) {
        resolve(null);
        return;
      }

      clearTimers();

      mediaRecorderRef.current.onstop = () => {
        const mimeType = mediaRecorderRef.current?.mimeType || 'audio/webm';
        const blob = new Blob(chunksRef.current, { type: mimeType });
        chunksRef.current = [];
        setIsRecording(false);
        setVolume(0);
        setFrequencyData(null);
        stopMediaStream();
        resolve(blob);
      };

      mediaRecorderRef.current.stop();
    });
  }, [isRecording, clearTimers, stopMediaStream]);

  const cancelRecording = useCallback(() => {
    clearTimers();
    
    if (mediaRecorderRef.current && mediaRecorderRef.current.state !== 'inactive') {
      mediaRecorderRef.current.stop();
    }
    
    chunksRef.current = [];
    setIsRecording(false);
    setVolume(0);
    setFrequencyData(null);
    stopMediaStream();
  }, [clearTimers, stopMediaStream]);

  // Start monitoring when recording starts
  useEffect(() => {
    if (isRecording && analyzerRef.current) {
      monitorAudio();
    }
    
    return () => {
      if (animationFrameRef.current) {
        cancelAnimationFrame(animationFrameRef.current);
      }
    };
  }, [isRecording, monitorAudio]);

  // Cleanup on unmount
  useEffect(() => {
    return () => {
      clearTimers();
      stopMediaStream();
    };
  }, [clearTimers, stopMediaStream]);

  return {
    isRecording,
    isPaused,
    volume,
    countdown,
    frequencyData,
    startRecording,
    stopRecording,
    cancelRecording,
  };
}
