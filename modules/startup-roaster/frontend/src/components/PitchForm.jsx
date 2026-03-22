import { useState } from 'react';

const MAX_CHARS = 300;

export default function PitchForm({ onSubmit, isLoading }) {
  const [pitch, setPitch] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (pitch.trim() && pitch.length <= MAX_CHARS) {
      onSubmit(pitch.trim());
    }
  };

  const remaining = MAX_CHARS - pitch.length;
  const isOverLimit = remaining < 0;
  const isEmpty = !pitch.trim();

  return (
    <form onSubmit={handleSubmit} className="space-y-4">
      <div className="relative">
        <textarea
          value={pitch}
          onChange={(e) => setPitch(e.target.value)}
          placeholder="Describe your startup idea in 1-3 sentences... (e.g. 'Uber for dogs but on blockchain')"
          rows={4}
          className={`w-full px-4 py-3 rounded-xl border-2 text-gray-800 placeholder-gray-400 resize-none focus:outline-none focus:ring-2 transition-colors ${
            isOverLimit
              ? 'border-red-400 focus:ring-red-200'
              : 'border-gray-300 focus:ring-orange-200 focus:border-orange-400'
          }`}
          disabled={isLoading}
        />
        <span className={`absolute bottom-3 right-3 text-xs font-medium ${isOverLimit ? 'text-red-500' : 'text-gray-400'}`}>
          {remaining}
        </span>
      </div>

      <button
        type="submit"
        disabled={isEmpty || isOverLimit || isLoading}
        className="w-full py-3 px-6 bg-orange-500 text-white font-bold text-lg rounded-xl hover:bg-orange-600 disabled:opacity-40 disabled:cursor-not-allowed transition-colors shadow-md"
      >
        {isLoading ? 'Roasting...' : '🔥 Roast My Idea'}
      </button>
    </form>
  );
}
