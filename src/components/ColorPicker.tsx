'use client';

// Bottom-docked color palette + submit/clear action buttons.

import { motion } from 'framer-motion';
import type { PegColor, Difficulty } from '@/types/game';
import { PEG_COLORS, PEG_COLOR_STYLES, DIFFICULTY_CONFIGS } from '@/lib/constants';

interface Props {
  selectedColor: PegColor | null;
  difficulty: Difficulty;
  onSelectColor: (color: PegColor) => void;
  onSubmit: () => void;
  onClear: () => void;
  canSubmit: boolean;
}

export default function ColorPicker({
  selectedColor,
  difficulty,
  onSelectColor,
  onSubmit,
  onClear,
  canSubmit,
}: Props) {
  const cfg = DIFFICULTY_CONFIGS[difficulty];
  const colors = PEG_COLORS.slice(0, cfg.numColors);

  return (
    <div className="w-full max-w-sm mx-auto select-none">
      {/* Color swatches */}
      <div className="flex flex-wrap justify-center gap-2 sm:gap-3 mb-3">
        {colors.map((color, idx) => {
          const s = PEG_COLOR_STYLES[color];
          const active = selectedColor === color;
          return (
            <motion.button
              key={color}
              whileHover={{ scale: 1.18, y: -2 }}
              whileTap={{ scale: 0.88 }}
              onClick={() => onSelectColor(color)}
              aria-label={`${s.label} (key ${idx + 1})`}
              aria-pressed={active}
              className={`w-10 h-10 sm:w-11 sm:h-11 rounded-full border-2 transition-all duration-150 focus:outline-none ${
                active ? 'border-white' : 'border-transparent hover:border-white/40'
              }`}
              // Dynamic peg color — must use inline style (runtime value)
              style={{
                backgroundColor: s.bg,
                transform: active ? 'scale(1.12) translateY(-3px)' : undefined,
                boxShadow: active
                  ? `0 0 22px ${s.glow}, 0 0 44px ${s.ring}, inset 0 1px 0 rgba(255,255,255,0.4)`
                  : `0 0 7px ${s.ring}, inset 0 1px 0 rgba(255,255,255,0.15)`,
              }}
            >
              {active && (
                <span className="text-white/70 text-xs font-bold drop-shadow">✓</span>
              )}
            </motion.button>
          );
        })}
      </div>

      {/* Keyboard hint (desktop only) */}
      <div className="hidden sm:flex justify-center gap-3 mb-3">
        {colors.map((_, idx) => (
          <span key={idx} className="text-gray-500 text-[10px] font-mono">
            [{idx + 1}]
          </span>
        ))}
      </div>

      {/* Action buttons */}
      <div className="flex gap-3 justify-center">
        <motion.button
          whileHover={{ scale: 1.04 }}
          whileTap={{ scale: 0.96 }}
          onClick={onClear}
          className="px-5 py-2 rounded-xl bg-gray-700/50 text-gray-300 hover:bg-gray-600/50 hover:text-white border border-gray-600/30 hover:border-gray-400/50 transition-all text-sm font-medium"
        >
          Clear
        </motion.button>

        <motion.button
          whileHover={{ scale: canSubmit ? 1.04 : 1 }}
          whileTap={{ scale: canSubmit ? 0.96 : 1 }}
          onClick={onSubmit}
          disabled={!canSubmit}
          className={`px-8 py-2 rounded-xl font-bold text-sm transition-all duration-200 ${
            canSubmit
              ? 'bg-cyan-500 hover:bg-cyan-400 text-black shadow-lg shadow-cyan-500/50 cursor-pointer'
              : 'bg-gray-700/30 text-gray-600 cursor-not-allowed border border-gray-700/30'
          }`}
        >
          Submit
          <span className="hidden sm:inline text-[10px] opacity-50 ml-1">[↵]</span>
        </motion.button>
      </div>
    </div>
  );
}
