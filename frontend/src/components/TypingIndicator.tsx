import React from 'react';
import { motion } from 'framer-motion';

export const TypingIndicator: React.FC = () => {
  return (
    <motion.div
      initial={{ opacity: 0, y: 10 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -10 }}
      className="flex items-center gap-2 px-4"
    >
      <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
        <span className="text-sm">🐲</span>
      </div>
      <div className="bubble-assistant px-4 py-3 flex items-center gap-1">
        <span className="text-sm text-muted-foreground">Goku is thinking</span>
        <div className="flex gap-1 ml-1">
          <span className="w-1.5 h-1.5 rounded-full bg-primary typing-dot-1" />
          <span className="w-1.5 h-1.5 rounded-full bg-primary typing-dot-2" />
          <span className="w-1.5 h-1.5 rounded-full bg-primary typing-dot-3" />
        </div>
      </div>
    </motion.div>
  );
};

export default TypingIndicator;
