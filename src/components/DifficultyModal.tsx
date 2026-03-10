'use client';

// Full-screen start menu: mode selection, difficulty selection, and start button.

import { useState } from 'react';
import { motion } from 'framer-motion';
import type { Difficulty, GameMode } from '@/types/game';
import { DIFFICULTY_CONFIGS } from '@/lib/constants';

interface Props {
  onStart: (difficulty: Difficulty, mode: GameMode) => void;
  highScore: number;
}

const MODES: { mode: GameMode; emoji: string; label: string; desc: string }[] = [
  { mode: 'player-breaks', emoji: '🕵️', label: 'You Crack It', desc: "Break the AI's secret code" },
  { mode: 'ai-breaks',     emoji: '🤖', label: 'AI Cracks It', desc: 'Watch the AI break your code' },
];

const DIFFS: { d: Difficulty; ring: string }[] = [
  { d: 'easy',   ring: 'border-green-500 bg-green-500/10'  },
  { d: 'medium', ring: 'border-yellow-500 bg-yellow-500/10' },
  { d: 'hard',   ring: 'border-red-500 bg-red-500/10'      },
];

export default function DifficultyModal({ onStart, highScore }: Props) {
  const [diff, setDiff] = useState<Difficulty>('medium');
  const [mode, setMode] = useState<GameMode>('player-breaks');

  return (
    <div className="min-h-screen flex flex-col items-center justify-center p-4 overflow-y-auto bg-[#050010] text-white">
      {/* Title */}
      <motion.div
        initial={{ opacity: 0, y: -28 }}
        animate={{ opacity: 1, y: 0 }}
        className="text-center mb-8"
      >
        <h1
          className="text-5xl sm:text-7xl font-black tracking-widest leading-none mb-1"
          style={{
            background: 'linear-gradient(to right, #22d3ee, #a855f7, #ec4899)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent',
            backgroundClip: 'text',
            // Fallback for browsers that don't support bg-clip text
            color: '#22d3ee',
          }}
        >
          MASTERMIND
        </h1>
        <p className="text-cyan-400 text-xs tracking-[0.3em] uppercase mt-2 opacity-60">
          Crack the Code · Beat the AI
        </p>
        {highScore > 0 && (
          <motion.p
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.5 }}
            className="text-yellow-400 text-sm mt-3 font-mono"
          >
            🏆 Best Score: {highScore}
          </motion.p>
        )}
      </motion.div>

      {/* Mode selection */}
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.15 }}
        className="w-full max-w-md mb-5"
      >
        <h2 className="text-cyan-400 text-[10px] uppercase tracking-[0.2em] mb-2 text-center">
          Game Mode
        </h2>
        <div className="flex gap-3">
          {MODES.map(({ mode: m, emoji, label, desc }) => (
            <button
              key={m}
              onClick={() => setMode(m)}
              className={`flex-1 p-3 rounded-xl border transition-all duration-200 text-left ${
                mode === m
                  ? 'border-cyan-500 bg-cyan-500/10 text-white'
                  : 'border-gray-700/50 bg-gray-800/30 text-gray-400 hover:border-gray-500 hover:text-gray-200'
              }`}
            >
              <div className="font-semibold text-sm mb-0.5">
                {emoji} {label}
              </div>
              <div className="text-[11px] opacity-60">{desc}</div>
            </button>
          ))}
        </div>
      </motion.div>

      {/* Difficulty selection */}
      <motion.div
        initial={{ opacity: 0, y: 18 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.25 }}
        className="w-full max-w-md mb-8"
      >
        <h2 className="text-cyan-400 text-[10px] uppercase tracking-[0.2em] mb-2 text-center">
          Difficulty
        </h2>
        <div className="flex gap-3">
          {DIFFS.map(({ d, ring }) => {
            const cfg = DIFFICULTY_CONFIGS[d];
            return (
              <button
                key={d}
                onClick={() => setDiff(d)}
                className={`flex-1 p-3 rounded-xl border transition-all duration-200 ${
                  diff === d
                    ? ring + ' text-white'
                    : 'border-gray-700/50 bg-gray-800/30 text-gray-400 hover:border-gray-500 hover:text-gray-200'
                }`}
              >
                <div className="font-bold text-sm mb-0.5">{cfg.label}</div>
                <div className="text-[11px] opacity-60">{cfg.description}</div>
                <div className="text-[10px] opacity-40 mt-1">×{cfg.scoreMultiplier} pts</div>
              </button>
            );
          })}
        </div>
      </motion.div>

      {/* Start button */}
      <motion.button
        initial={{ opacity: 0, scale: 0.85 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.35 }}
        whileHover={{ scale: 1.06 }}
        whileTap={{ scale: 0.94 }}
        onClick={() => onStart(diff, mode)}
        className="px-14 py-4 bg-gradient-to-r from-cyan-500 to-purple-600 rounded-2xl text-black font-black text-lg tracking-[0.15em] shadow-2xl shadow-cyan-500/40 hover:shadow-cyan-400/60 transition-shadow"
      >
        START GAME
      </motion.button>

      {/* Controls hint */}
      <motion.div
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.55 }}
        className="mt-8 text-center space-y-1"
      >
        <p className="text-gray-400 text-[11px]">
          <span className="text-gray-500">1–8</span> select color ·{' '}
          <span className="text-gray-500">Enter</span> submit ·{' '}
          <span className="text-gray-500">Backspace</span> remove ·{' '}
          <span className="text-gray-500">P</span> pause
        </p>
        <p className="text-gray-400 text-[11px]">Touch: tap a color, then tap a slot</p>
      </motion.div>
    </div>
  );
}
