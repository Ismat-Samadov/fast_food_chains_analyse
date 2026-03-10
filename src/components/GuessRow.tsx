'use client';

// A single completed guess row: colored pegs on the left, feedback grid on the right.

import { motion } from 'framer-motion';
import type { GuessEntry } from '@/types/game';
import { PEG_COLOR_STYLES } from '@/lib/constants';
import FeedbackPegs from './FeedbackPegs';

interface Props {
  guess: GuessEntry;
  rowIndex: number;
  codeLength: number;
  isLatest: boolean;
}

export default function GuessRow({ guess, rowIndex, codeLength, isLatest }: Props) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -24 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.28, delay: 0.03 }}
      className={`flex items-center gap-3 px-2 py-[6px] rounded-xl ${
        isLatest ? 'bg-white/5 border border-cyan-500/20' : ''
      }`}
    >
      {/* Row number */}
      <span className="text-gray-400 text-xs font-mono w-5 text-right flex-shrink-0">
        {rowIndex + 1}
      </span>

      {/* Colored pegs */}
      <div className="flex items-center gap-2">
        {guess.pegs.slice(0, codeLength).map((color, i) => {
          const style = PEG_COLOR_STYLES[color];
          return (
            <motion.div
              key={i}
              initial={{ scale: 0 }}
              animate={{ scale: 1 }}
              transition={{ duration: 0.18, delay: i * 0.04 }}
              className="w-8 h-8 rounded-full border-2 border-white/20 flex-shrink-0"
              // Dynamic peg color — must use inline style (runtime value)
              style={{
                backgroundColor: style.bg,
                boxShadow: `0 0 10px ${style.glow}, inset 0 1px 0 rgba(255,255,255,0.3)`,
              }}
            />
          );
        })}
      </div>

      {/* Feedback pegs */}
      <div className="ml-auto flex-shrink-0">
        <FeedbackPegs
          blacks={guess.feedback.blacks}
          whites={guess.feedback.whites}
          codeLength={codeLength}
        />
      </div>
    </motion.div>
  );
}
