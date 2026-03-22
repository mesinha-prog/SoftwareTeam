const SCORE_CONFIG = {
  1: { emoji: '💀', bg: 'bg-red-100', border: 'border-red-400', text: 'text-red-700' },
  2: { emoji: '🔥', bg: 'bg-orange-100', border: 'border-orange-400', text: 'text-orange-700' },
  3: { emoji: '😐', bg: 'bg-yellow-100', border: 'border-yellow-400', text: 'text-yellow-700' },
  4: { emoji: '💎', bg: 'bg-blue-100', border: 'border-blue-400', text: 'text-blue-700' },
  5: { emoji: '🦄', bg: 'bg-green-100', border: 'border-green-400', text: 'text-green-700' },
};

export default function RoastScore({ score, scoreLabel }) {
  const config = SCORE_CONFIG[score] ?? SCORE_CONFIG[3];
  return (
    <div className={`inline-flex flex-col items-center gap-1 px-8 py-4 rounded-2xl border-2 ${config.bg} ${config.border}`}>
      <span className="text-5xl">{config.emoji}</span>
      <span className={`text-xl font-bold ${config.text}`}>{scoreLabel}</span>
      <span className={`text-sm font-medium ${config.text} opacity-70`}>Roast Score</span>
    </div>
  );
}
