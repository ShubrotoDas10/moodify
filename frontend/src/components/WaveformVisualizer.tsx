import React, { useMemo } from 'react';
import { motion } from 'framer-motion';

interface WaveformVisualizerProps {
  frequencyData: Uint8Array | null;
  volume: number;
  isRecording: boolean;
  barCount?: number;
}

export const WaveformVisualizer: React.FC<WaveformVisualizerProps> = ({
  frequencyData,
  volume,
  isRecording,
  barCount = 32,
}) => {
  const bars = useMemo(() => {
    if (!frequencyData || !isRecording) {
      return Array(barCount).fill(0.1);
    }

    const step = Math.floor(frequencyData.length / barCount);
    const normalized: number[] = [];

    for (let i = 0; i < barCount; i++) {
      const index = i * step;
      const value = frequencyData[index] / 255;
      normalized.push(Math.max(0.1, value));
    }

    return normalized;
  }, [frequencyData, isRecording, barCount]);

  return (
    <div className="flex items-center justify-center gap-1 h-12 px-4">
      {bars.map((height, index) => (
        <motion.div
          key={index}
          className="w-1 rounded-full bg-gradient-to-t from-primary to-dbz-gold"
          initial={{ height: 4 }}
          animate={{
            height: isRecording ? height * 48 : 4,
            opacity: isRecording ? 0.7 + height * 0.3 : 0.3,
          }}
          transition={{
            duration: 0.1,
            ease: 'easeOut',
          }}
          style={{
            boxShadow: isRecording && height > 0.5 
              ? '0 0 8px hsl(22 100% 55% / 0.5)' 
              : 'none',
          }}
        />
      ))}
    </div>
  );
};

export default WaveformVisualizer;
