import React, { useEffect, useRef } from 'react';
import { ScrollArea } from "@/components/ui/scroll-area";
import MessageBubble from './MessageBubble';
import TypingIndicator from './TypingIndicator';

interface ChatContainerProps {
  messages: any[];
  isTyping?: boolean;
}

const ChatContainer: React.FC<ChatContainerProps> = ({ messages, isTyping }) => {
  const scrollRef = useRef<HTMLDivElement>(null);

  // Auto-scroll logic jab naye messages aayein
  useEffect(() => {
    if (scrollRef.current) {
      const scrollElement = scrollRef.current.querySelector('[data-radix-scroll-area-viewport]');
      if (scrollElement) {
        scrollElement.scrollTop = scrollElement.scrollHeight;
      }
    }
  }, [messages, isTyping]);

  return (
    <ScrollArea ref={scrollRef} className="h-full w-full pr-4">
      <div className="flex flex-col gap-4 py-4">
        {messages.map((msg, index) => (
          <MessageBubble 
            // Unique key for React performance
            key={msg.id || `msg-${index}-${Date.now()}`} 
            // FIX: Using 'msg' instead of undefined 'message'
            message={msg.timestamp ? msg : { ...msg, timestamp: new Date() }} 
          />
        ))}
        {isTyping && <TypingIndicator />}
      </div>
    </ScrollArea>
  );
};

export default ChatContainer;