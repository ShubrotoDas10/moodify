import React, { useState, useCallback, useEffect } from 'react';
import CharacterDisplay, { EmotionType } from '@/components/CharacterDisplay';
import ChatContainer from '@/components/ChatContainer';
import RecordButton from '@/components/RecordButton';
import { useVoiceRecorder } from '@/hooks/useVoiceRecorder';
import { sendAudioMessage } from '@/lib/api';
import { toast } from "sonner";

const Index: React.FC = () => {
  const [messages, setMessages] = useState<any[]>([]);
  const [currentEmotion, setCurrentEmotion] = useState<EmotionType>('neutral');
  const [isTalking, setIsTalking] = useState(false);
  const [isProcessing, setIsProcessing] = useState(false);

  // Goku ki awaaz nikalne ke liye function
  const speakReply = (text: string) => {
    window.speechSynthesis.cancel();
    const utterance = new SpeechSynthesisUtterance(text);
    
    // Voice settings taaki Goku jaisa feel aaye
    utterance.pitch = 1.1;
    utterance.rate = 1.0;

    utterance.onstart = () => setIsTalking(true);
    utterance.onend = () => setIsTalking(false);
    window.speechSynthesis.speak(utterance);
  };

  const handleAudioSend = useCallback(async (audioBlob: Blob) => {
    setIsProcessing(true);
    try {
      // Backend ko audio bhejna (Hybrid analysis logic)
      const response = await sendAudioMessage(audioBlob);
      
      const userMsg = { 
        id: crypto.randomUUID(),
        type: 'user', 
        content: response.transcript, 
        timestamp: new Date() 
      };
      
      const aiMsg = { 
        id: crypto.randomUUID(),
        type: 'assistant', 
        content: response.chat_response.message, 
        emotion: response.emotion.label as EmotionType,
        timestamp: new Date() 
      };

      setMessages(prev => [...prev, userMsg, aiMsg]);
      
      // Emotion update hote hi CharacterDisplay ka background badal jayega
      setCurrentEmotion(response.emotion.label as EmotionType);
      
      // Goku reply dega
      speakReply(response.chat_response.message);
      
    } catch (e: any) {
      console.error("Audio failed:", e);
      // Agar backend 500 error de (jaise config issue) toh toast dikhao
      toast.error(e.response?.data?.detail || "Goku is training right now, try later!");
    } finally {
      setIsProcessing(false);
    }
  }, []);

  const { isRecording, startRecording, stopRecording } = useVoiceRecorder({
    onAutoSend: handleAudioSend,
  });

  return (
    // Main Container: Relative and Screen size
    <div className="relative h-screen w-full overflow-hidden bg-black">
      
      {/* 1. LAYER: CHARACTER & BACKGROUND AURA
          Isko z-0 par rakha hai taaki ye sabse piche rahe
      */}
      <div className="absolute inset-0 z-0">
        <CharacterDisplay emotion={currentEmotion} isTalking={isTalking} />
      </div>

      {/* 2. LAYER: UI OVERLAY (Chat & Controls)
          Bg-transparent zaroori hai taaki piche ka aura dikhe
      */}
      <main className="relative z-10 flex flex-col h-full bg-transparent pointer-events-none">
        
        {/* Header */}
        <header className="p-6 pointer-events-auto">
          <h1 className="text-orange-600 font-black text-3xl tracking-tighter drop-shadow-lg">
            MOODIFY
          </h1>
        </header>
        
        {/* Chat Messages Section */}
        <div className="flex-1 overflow-hidden px-4 md:px-20 pointer-events-auto">
          <div className="h-full flex flex-col justify-end pb-6">
             <ChatContainer messages={messages} isTyping={isProcessing} />
          </div>
        </div>

        {/* Recording Controls */}
        <div className="h-44 flex flex-col items-center justify-center pb-12 pointer-events-auto">
          <RecordButton
            isRecording={isRecording}
            isProcessing={isProcessing}
            onStart={startRecording}
            onStop={async () => {
              const blob = await stopRecording();
              if (blob) await handleAudioSend(blob);
            }}
          />
          <p className="mt-3 text-xs font-bold uppercase tracking-widest text-white/40">
            {isRecording ? "Listening to your spirit..." : "Tap to talk to Goku"}
          </p>
        </div>
      </main>

      {/* Subtle Vignette effect for depth */}
      <div className="absolute inset-0 pointer-events-none bg-[radial-gradient(circle_at_center,transparent_0%,rgba(0,0,0,0.5)_100%)] z-5" />
    </div>
  );
};

export default Index;