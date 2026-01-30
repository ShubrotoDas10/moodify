import React from 'react';
import { cn } from "@/lib/utils";
// CharacterDisplay se helpers import karein
import { getCharacterImage, getEmotionEmoji, EmotionType } from './CharacterDisplay';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp?: Date;
  emotion?: EmotionType;
}

interface MessageBubbleProps {
  message: Message;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message }) => {
  const isAssistant = message.type === 'assistant';

  const formatTime = (date?: Date) => {
    if (!date) return "";
    return new Date(date).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
  };

  return (
    <div className={cn(
      "flex w-full mb-4 animate-in fade-in slide-in-from-bottom-2",
      isAssistant ? "justify-start" : "justify-end"
    )}>
      <div className={cn(
        "flex max-w-[80%] items-end gap-2",
        isAssistant ? "flex-row" : "flex-row-reverse"
      )}>
        {isAssistant && (
          <div className="w-8 h-8 rounded-full overflow-hidden bg-orange-500/20 border border-orange-500/50 flex-shrink-0">
            <img 
              src={getCharacterImage(message.emotion || 'neutral')} 
              alt="Avatar"
              className="w-full h-full object-cover"
            />
          </div>
        )}
        
        <div className={cn(
          "px-4 py-2 rounded-2xl text-sm shadow-lg",
          isAssistant 
            ? "bg-zinc-900 text-white rounded-bl-none border border-white/10" 
            : "bg-orange-600 text-white rounded-br-none"
        )}>
          <p className="leading-relaxed">{message.content}</p>
          <div className="flex items-center justify-end gap-2 mt-1 opacity-50 text-[10px]">
            {isAssistant && message.emotion && (
              <span>{getEmotionEmoji(message.emotion)} {message.emotion}</span>
            )}
            <span>{formatTime(message.timestamp)}</span>
          </div>
        </div>
      </div>
    </div>
  );
};

export default MessageBubble;