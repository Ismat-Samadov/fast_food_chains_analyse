'use client';

// Animated win/lose overlay with secret code reveal and score display.

import { motion } from 'framer-motion';
import type { PegColor, GameStatus } from '@/types/game';
import { PEG_COLOR_STYLES } from '@/lib/constants';

interface Props {
  status: GameStatus;
  score: number;
  highScore: number;
  isNewHighScore: boolean;
  guessCount: number;
  secretCode: (PegColor | null)[];
  mode: string;
  onPlayAgain: () => void;
  onMenu: () => void;
}

export default function EndScreen({
  status,
  score,
  highScore,
  isNewHighScore,
  guessCount,
  secretCode,
  mode,
  onPlayAgain,
  onMenu,
}: Props) {
  const won = status === 'won';

  const title = won
    ? mode === 'ai-breaks' ? 'CODE UNBROKEN!' : 'CODE CRACKED!'
    : mode === 'ai-breaks' ? 'AI WINS!' : 'GAME OVER';

  const subtitle = won
    ? mode === 'ai-breaks'
      ? `The AI couldn't crack your code in ${guessCount} guess${guessCount !== 1 ? 'es' : ''}!`
      : `You cracked it in ${guessCount} guess${guessCount !== 1 ? 'es' : ''}!`
    : mode === 'ai-breaks'
    ? 'The AI decoded your secret!'
    : "The code was too clever this time.";

  return (
    <motion.div
      initial={{ opacity: 0 }}
      animate={{ opacity: 1 }}
      exit={{ opacity: 0 }}
      className="fixed inset-0 bg-black/80 backdrop-blur-md flex items-center justify-center z-50 p-4"
    >
      <motion.div
        initial={{ scale: 0.5, opacity: 0, y: 40 }}
        animate={{ scale: 1, opacity: 1, y: 0 }}
        exit={{ scale: 0.8, opacity: 0 }}
        transition={{ type: 'spring', stiffness: 220, damping: 22 }}
        className={`bg-gray-950/98 border rounded-2xl p-6 sm:p-8 max-w-sm w-full text-center shadow-2xl ${
          won ? 'border-cyan-500/50 shadow-cyan-500/20' : 'border-red-500/40 shadow-red-500/15'
        }`}
      >
        {/* Icon */}
        <motion.div
          initial={{ scale: 0, rotate: -180 }}
          animate={{ scale: 1, rotate: 0 }}
          transition={{ delay: 0.15, type: 'spring', stiffness: 280 }}
          className="text-5xl mb-4"
        >
          {won ? '🎉' : '💀'}
        </motion.div>

        {/* Heading */}
        <motion.h2
          initial={{ opacity: 0, y: -8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.25 }}
          className={`text-2xl font-black tracking-wider mb-1 ${
            won ? 'text-cyan-400' : 'text-red-400'
          }`}
        >
          {title}
        </motion.h2>
        <motion.p
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ delay: 0.32 }}
          className="text-gray-400 text-sm mb-5"
        >
          {subtitle}
        </motion.p>

        {/* Secret code reveal */}
        <motion.div
          initial={{ opacity: 0, y: 8 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.42 }}
          className="mb-5"
        >
          <p className="text-gray-400 text-[10px] uppercase tracking-widest mb-2">
            The Secret Code
          </p>
          <div className="flex justify-center gap-2">
            {secretCode.map((color, i) => {
              const s = color ? PEG_COLOR_STYLES[color] : null;
              return (
                <motion.div
                  key={i}
                  initial={{ scale: 0, rotate: 180 }}
                  animate={{ scale: 1, rotate: 0 }}
                  transition={{ delay: 0.52 + i * 0.08, type: 'spring', stiffness: 260 }}
                  className="w-10 h-10 rounded-full border-2 border-white/20"
                  // Dynamic peg color — must use inline style (runtime value)
                  style={
                    s
                      ? { backgroundColor: s.bg, boxShadow: `0 0 14px ${s.glow}` }
                      : { backgroundColor: 'rgba(255,255,255,0.06)' }
                  }
                />
              );
            })}
          </div>
        </motion.div>

        {/* Score */}
        {won && score > 0 && (
          <motion.div
            initial={{ opacity: 0, scale: 0.7 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ delay: 0.75 }}
            className="mb-5"
          >
            <div className="text-yellow-400 text-3xl font-black">+{score}</div>
            <div className="text-yellow-700 text-[10px] uppercase tracking-widest">points</div>
            {isNewHighScore && (
              <motion.p
                initial={{ scale: 0 }}
                animate={{ scale: 1 }}
                transition={{ delay: 0.95, type: 'spring' }}
                className="mt-1 text-yellow-300 text-xs font-bold"
              >
                🏆 NEW HIGH SCORE!
              </motion.p>
            )}
          </motion.div>
        )}

        {/* Buttons */}
        <div className="flex gap-3 mt-2">
          <motion.button
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            onClick={onMenu}
            className="flex-1 py-3 rounded-xl bg-gray-800/70 text-gray-300 hover:bg-gray-700/70 hover:text-white border border-gray-700/30 transition-all text-sm font-semibold"
          >
            Menu
          </motion.button>
          <motion.button
            whileHover={{ scale: 1.04 }}
            whileTap={{ scale: 0.96 }}
            onClick={onPlayAgain}
            className={`flex-1 py-3 rounded-xl font-bold text-sm transition-all ${
              won
                ? 'bg-cyan-500 hover:bg-cyan-400 text-black shadow-lg shadow-cyan-500/40'
                : 'bg-red-500/80 hover:bg-red-400 text-white shadow-lg shadow-red-500/25'
            }`}
          >
            Play Again
          </motion.button>
        </div>
      </motion.div>
    </motion.div>
  );
}
