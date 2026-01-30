import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Mic, MicOff, Loader2 } from 'lucide-react';

// Interface matching with Index.tsx props
interface RecordButtonProps {
  isRecording: boolean;
  isProcessing: boolean;
  onStart: () => void;
  onStop: () => void;
}

const RecordButton: React.FC<RecordButtonProps> = ({
  isRecording,
  isProcessing,
  onStart,
  onStop,
}) => {
  return (
    <div className="flex flex-col items-center gap-3">
      <motion.button
        // Direct trigger for start/stop based on recording state
        onClick={isRecording ? onStop : onStart}
        disabled={isProcessing}
        className={`relative w-24 h-24 rounded-full flex items-center justify-center transition-all shadow-lg outline-none
          ${isRecording 
            ? 'bg-red-600 shadow-red-500/50 recording-active' 
            : 'bg-orange-500 shadow-orange-500/50'
          }
          ${isProcessing ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}
        `}
        whileHover={{ scale: isProcessing ? 1 : 1.05 }}
        whileTap={{ scale: isProcessing ? 1 : 0.95 }}
      >
        {/* Pulsing rings animation only when recording */}
        <AnimatePresence>
          {isRecording && (
            <motion.div
              className="absolute inset-0 rounded-full bg-red-500"
              initial={{ scale: 1, opacity: 0.6 }}
              animate={{ scale: 1.8, opacity: 0 }}
              transition={{ duration: 1, repeat: Infinity }}
            />
          )}
        </AnimatePresence>

        {/* Dynamic Icon Display */}
        <div className="relative z-10 text-white">
          {isProcessing ? (
            <Loader2 className="w-10 h-10 animate-spin" />
          ) : isRecording ? (
            <MicOff className="w-10 h-10" />
          ) : (
            <Mic className="w-10 h-10" />
          )}
        </div>
      </motion.button>

      {/* Status text synced with button state */}
      <span className="text-sm font-bold text-white/50 tracking-widest uppercase">
        {isProcessing ? "Processing..." : isRecording ? "Stop Recording" : "Tap to Talk"}
      </span>
    </div>
  );
};

export default RecordButton;