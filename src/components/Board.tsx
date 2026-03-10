'use client';

// The main game board: past guesses + the active input row + empty future rows.

import { useRef, useEffect } from 'react';
import { motion } from 'framer-motion';
import type { PegColor, GuessEntry } from '@/types/game';
import { PEG_COLOR_STYLES, DIFFICULTY_CONFIGS } from '@/lib/constants';
import GuessRow from './GuessRow';
import FeedbackPegs from './FeedbackPegs';

interface Props {
  guesses: GuessEntry[];
  currentGuess: (PegColor | null)[];
  activeSlot: number;
  selectedColor: PegColor | null;
  difficulty: string;
  status: string;
  onSlotClick: (index: number) => void;
}

export default function Board({
  guesses,
  currentGuess,
  activeSlot,
  selectedColor,
  difficulty,
  status,
  onSlotClick,
}: Props) {
  const cfg = DIFFICULTY_CONFIGS[difficulty];
  const bottomRef = useRef<HTMLDivElement>(null);

  // Auto-scroll to keep the active row visible
  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth', block: 'nearest' });
  }, [guesses.length]);

  const remaining = cfg.maxGuesses - guesses.length;

  return (
    <div className="flex flex-col gap-[6px] w-full">
      {/* Completed guess rows */}
      {guesses.map((guess, i) => (
        <GuessRow
          key={i}
          guess={guess}
          rowIndex={i}
          codeLength={cfg.codeLength}
          isLatest={i === guesses.length - 1}
        />
      ))}

      {/* Active input row */}
      {status === 'playing' && (
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          className="flex items-center gap-3 px-2 py-[6px] rounded-xl border border-cyan-400/40 bg-cyan-500/5"
        >
          <span className="text-cyan-400 text-xs font-mono font-bold w-5 text-right flex-shrink-0">
            {guesses.length + 1}
          </span>

          <div className="flex items-center gap-2">
            {currentGuess.slice(0, cfg.codeLength).map((color, i) => {
              const isActive = activeSlot === i;
              const style = color ? PEG_COLOR_STYLES[color] : null;

              return (
                <motion.button
                  key={i}
                  whileHover={{ scale: 1.12 }}
                  whileTap={{ scale: 0.92 }}
                  onClick={() => onSlotClick(i)}
                  aria-label={`Slot ${i + 1}${color ? `: ${PEG_COLOR_STYLES[color].label}` : ' (empty)'}`}
                  className={`w-8 h-8 sm:w-9 sm:h-9 rounded-full border-2 flex-shrink-0 transition-all cursor-pointer focus:outline-none ${
                    isActive
                      ? 'border-cyan-400'
                      : 'border-white/20 hover:border-white/50'
                  }`}
                  // Dynamic peg color — must use inline style (runtime value)
                  style={
                    style
                      ? {
                          backgroundColor: style.bg,
                          boxShadow: isActive
                            ? `0 0 16px ${style.glow}, 0 0 6px rgba(0,255,255,0.5), inset 0 1px 0 rgba(255,255,255,0.3)`
                            : `0 0 10px ${style.glow}, inset 0 1px 0 rgba(255,255,255,0.3)`,
                        }
                      : {
                          backgroundColor: isActive
                            ? 'rgba(0,255,255,0.08)'
                            : 'rgba(255,255,255,0.04)',
                          boxShadow: isActive ? '0 0 12px rgba(0,255,255,0.3)' : 'none',
                        }
                  }
                />
              );
            })}
          </div>

          {/* Ghost feedback grid */}
          <div className="ml-auto flex-shrink-0 opacity-20">
            <FeedbackPegs blacks={0} whites={0} codeLength={cfg.codeLength} />
          </div>
        </motion.div>
      )}

      {/* Empty upcoming rows */}
      {status === 'playing' &&
        Array.from({ length: Math.max(0, remaining - 1) }).map((_, i) => (
          <div
            key={`empty-${i}`}
            className="flex items-center gap-3 px-2 py-[6px] rounded-xl opacity-15"
          >
            <span className="text-gray-500 text-xs font-mono w-5 text-right flex-shrink-0">
              {guesses.length + i + 2}
            </span>
            <div className="flex items-center gap-2">
              {Array.from({ length: cfg.codeLength }).map((_, j) => (
                <div
                  key={j}
                  className="w-8 h-8 sm:w-9 sm:h-9 rounded-full border border-gray-700/40"
                  style={{ backgroundColor: 'rgba(255,255,255,0.02)' }}
                />
              ))}
            </div>
            <div className="ml-auto flex-shrink-0">
              <FeedbackPegs blacks={0} whites={0} codeLength={cfg.codeLength} />
            </div>
          </div>
        ))}

      <div ref={bottomRef} />
    </div>
  );
}
