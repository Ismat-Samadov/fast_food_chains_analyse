'use client';

// AI-breaks mode view: shows the player's secret code and the AI's step-by-step guesses.

import { motion } from 'framer-motion';
import type { GuessEntry, PegColor, Difficulty } from '@/types/game';
import { PEG_COLOR_STYLES, DIFFICULTY_CONFIGS } from '@/lib/constants';
import GuessRow from './GuessRow';

interface Props {
  aiGuesses: GuessEntry[];
  playerCode: (PegColor | null)[];
  difficulty: Difficulty;
  status: string;
  onStep: () => void;
}

export default function AiBreaker({ aiGuesses, playerCode, difficulty, status, onStep }: Props) {
  const cfg = DIFFICULTY_CONFIGS[difficulty];
  const canStep = status === 'playing' && aiGuesses.length < cfg.maxGuesses;
  const done = status === 'won' || status === 'lost';

  return (
    <div className="flex flex-col items-center gap-4 w-full max-w-sm mx-auto py-2">
      {/* Player's code display */}
      <div className="text-center">
        <p className="text-gray-400 text-[10px] uppercase tracking-widest mb-2">Your Secret Code</p>
        <div className="flex justify-center gap-2">
          {playerCode.slice(0, cfg.codeLength).map((color, i) => {
            const s = color ? PEG_COLOR_STYLES[color] : null;
            return (
              <div
                key={i}
                className="w-9 h-9 rounded-full border-2 border-white/25"
                // Dynamic peg color — must use inline style (runtime value)
                style={
                  s
                    ? { backgroundColor: s.bg, boxShadow: `0 0 12px ${s.glow}` }
                    : { backgroundColor: 'rgba(255,255,255,0.06)' }
                }
              />
            );
          })}
        </div>
      </div>

      {/* AI guess history */}
      {aiGuesses.length > 0 && (
        <div className="w-full space-y-[5px]">
          {aiGuesses.map((guess, i) => (
            <GuessRow
              key={i}
              guess={guess}
              rowIndex={i}
              codeLength={cfg.codeLength}
              isLatest={i === aiGuesses.length - 1}
            />
          ))}
        </div>
      )}

      {/* AI thinking indicator */}
      {canStep && aiGuesses.length > 0 && (
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="text-cyan-400 text-xs"
        >
          🤖 Analysing…
        </motion.p>
      )}

      {/* Step / Start button */}
      {canStep && (
        <motion.button
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={onStep}
          className="px-8 py-3 bg-purple-600 hover:bg-purple-500 text-white rounded-xl font-bold transition-all shadow-lg shadow-purple-500/30 mt-1"
        >
          {aiGuesses.length === 0 ? '🤖 Start AI' : '🤖 Next Guess'}
        </motion.button>
      )}

      {!canStep && !done && (
        <p className="text-red-400 text-sm">AI has exhausted all guesses!</p>
      )}
    </div>
  );
}
