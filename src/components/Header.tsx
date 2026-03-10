'use client';

// Top navigation bar: logo, live game stats, and control toggles.

import type { GameStatus } from '@/types/game';

interface Props {
  score: number;
  highScore: number;
  guessCount: number;
  maxGuesses: number;
  time: number;
  status: GameStatus;
  soundEnabled: boolean;
  musicEnabled: boolean;
  onToggleSound: () => void;
  onToggleMusic: () => void;
  onPause: () => void;
  onMenu: () => void;
}

function fmt(s: number) {
  return `${String(Math.floor(s / 60)).padStart(2, '0')}:${String(s % 60).padStart(2, '0')}`;
}

export default function Header({
  score,
  highScore,
  guessCount,
  maxGuesses,
  time,
  status,
  soundEnabled,
  musicEnabled,
  onToggleSound,
  onToggleMusic,
  onPause,
  onMenu,
}: Props) {
  const inGame = status === 'playing' || status === 'paused';

  return (
    <header className="w-full flex items-center justify-between px-4 py-2 border-b border-cyan-500/20 bg-black/50 backdrop-blur-md flex-shrink-0 z-10">
      {/* Logo */}
      <button
        onClick={onMenu}
        className="flex items-center gap-2 group"
        aria-label="Go to main menu"
      >
        <div className="w-7 h-7 rounded-lg bg-gradient-to-br from-cyan-400 to-purple-600 flex items-center justify-center text-black font-black text-xs shadow-md shadow-cyan-500/40">
          M
        </div>
        <span className="text-cyan-400 font-black text-base tracking-widest hidden sm:block group-hover:text-cyan-300 transition-colors">
          MASTERMIND
        </span>
      </button>

      {/* Live stats */}
      {inGame && (
        <div className="flex items-center gap-4 sm:gap-6">
          <div className="text-center">
            <div className="text-[9px] text-cyan-400 uppercase tracking-widest">Guess</div>
            <div className="text-cyan-300 font-mono font-bold text-sm">
              {guessCount}/{maxGuesses}
            </div>
          </div>
          <div className="text-center">
            <div className="text-[9px] text-cyan-400 uppercase tracking-widest">Time</div>
            <div className="text-cyan-300 font-mono font-bold text-sm">{fmt(time)}</div>
          </div>
          <div className="text-center">
            <div className="text-[9px] text-cyan-400 uppercase tracking-widest">Score</div>
            <div className="text-yellow-400 font-mono font-bold text-sm">{score}</div>
          </div>
        </div>
      )}

      {/* Controls */}
      <div className="flex items-center gap-1">
        {highScore > 0 && !inGame && (
          <div className="hidden md:flex items-center gap-1 mr-2 text-yellow-400 text-xs">
            <span className="opacity-60">BEST</span>
            <span className="font-mono font-bold">{highScore}</span>
          </div>
        )}

        <button
          onClick={onToggleMusic}
          title={musicEnabled ? 'Music on' : 'Music off'}
          aria-pressed={musicEnabled}
          className={`p-2 rounded-lg transition-all text-base ${
            musicEnabled ? 'text-cyan-400 bg-cyan-400/15' : 'text-gray-600 hover:text-gray-400'
          }`}
        >
          🎵
        </button>

        <button
          onClick={onToggleSound}
          title={soundEnabled ? 'Sound on' : 'Sound off'}
          aria-pressed={soundEnabled}
          className={`p-2 rounded-lg transition-all text-base ${
            soundEnabled ? 'text-cyan-400 bg-cyan-400/15' : 'text-gray-600 hover:text-gray-400'
          }`}
        >
          {soundEnabled ? '🔊' : '🔇'}
        </button>

        {status === 'playing' && (
          <button
            onClick={onPause}
            title="Pause (P)"
            className="p-2 rounded-lg text-gray-500 hover:text-white hover:bg-white/10 transition-all text-base"
          >
            ⏸
          </button>
        )}
      </div>
    </header>
  );
}
