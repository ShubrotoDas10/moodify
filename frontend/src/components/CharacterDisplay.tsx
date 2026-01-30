import React from 'react';
import gokuBase from '../assets/characters/goku-base.png';
import gokuHappy from '../assets/characters/goku-super-saiyan.png';
import gokuSad from '../assets/characters/goku-sad.png';
import gokuAngry from '../assets/characters/vegeta-annoyed.png';
import gokuSurprised from '../assets/characters/goku-shocked.png';
import gokuShocked from '../assets/characters/goku-ultra-instinct.png';
import gokuInjured from '../assets/characters/goku-injured.png';

export type EmotionType = string;

export const getCharacterImage = (emotion: string): string => {
  const e = emotion.toLowerCase();
  if (e.includes('happy') || e.includes('happiness')) return gokuHappy;
  if (e.includes('angry') || e.includes('anger')) return gokuAngry;
  if (e.includes('sad')) return gokuSad;
  if (e.includes('surprised')) return gokuSurprised;
  if (e.includes('shocked')) return gokuShocked;
  if (e.includes('injured')) return gokuInjured;
  return gokuBase;
};

export const getEmotionEmoji = (emotion: string): string => {
  const e = emotion.toLowerCase();
  if (e.includes('happy') || e.includes('happiness')) return '😊';
  if (e.includes('angry') || e.includes('anger')) return '😠';
  if (e.includes('sad')) return '😢';
  if (e.includes('surprised')) return '😲';
  if (e.includes('shocked')) return '😱';
  if (e.includes('injured')) return '🤕';
  return '😐';
};

const getAuraColor = (emotion: string) => {
  const e = emotion.toLowerCase();
  if (e.includes('angry') || e.includes('anger')) return 'rgba(220, 38, 38, 0.4)';
  if (e.includes('happy') || e.includes('happiness')) return 'rgba(250, 204, 21, 0.3)';
  return 'rgba(249, 115, 22, 0.2)';
};

interface CharacterDisplayProps {
  emotion: string;
  isTalking?: boolean;
}

const CharacterDisplay: React.FC<CharacterDisplayProps> = ({ emotion, isTalking }) => {
  const charImage = getCharacterImage(emotion);
  const auraColor = getAuraColor(emotion);

  return (
    <div className="absolute inset-0 flex items-center justify-center overflow-hidden bg-black">
      {/* 1. Static Aura (No Vibration) */}
      <div 
        className="absolute w-full h-full blur-[150px] transition-colors duration-1000"
        style={{ backgroundColor: auraColor }}
      />
      
      {/* 2. Goku Main Image (Now 100% Steady) */}
      <div className="relative flex flex-col items-center justify-center h-full w-full">
        <img 
          key={charImage}
          src={charImage} 
          alt="Goku" 
          className="max-h-[80vh] w-auto object-contain drop-shadow-[0_0_35px_rgba(0,0,0,0.7)]"
        />

        {/* 3. Soundwave Overlay (Only shows when talking) */}
        {isTalking && (
          <div className="absolute bottom-20 flex items-end gap-1 h-12">
            {[...Array(15)].map((_, i) => (
              <div 
                key={i}
                className="w-1 bg-orange-500 rounded-full animate-soundwave"
                style={{ 
                  height: '20%',
                  animationDelay: `${i * 0.05}s` 
                }}
              />
            ))}
          </div>
        )}
      </div>

      {/* Soundwave CSS */}
      <style>{`
        @keyframes soundwave {
          0%, 100% { height: 20%; }
          50% { height: 100%; }
        }
        .animate-soundwave {
          animation: soundwave 0.6s ease-in-out infinite;
        }
      `}</style>
    </div>
  );
};

export default CharacterDisplay;