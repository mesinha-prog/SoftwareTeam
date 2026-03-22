export default function SuggestionsSection({ suggestions }) {
  return (
    <div className="bg-orange-50 border border-orange-200 rounded-xl p-6">
      <h2 className="text-lg font-bold text-gray-800 mb-4">🛠️ How to Fix It</h2>
      <ul className="space-y-3">
        {suggestions.map((item, i) => (
          <li key={i} className="flex gap-3">
            <span className="text-orange-500 font-bold mt-0.5">{i + 1}.</span>
            <span className="text-gray-700 leading-relaxed">{item}</span>
          </li>
        ))}
      </ul>
    </div>
  );
}
