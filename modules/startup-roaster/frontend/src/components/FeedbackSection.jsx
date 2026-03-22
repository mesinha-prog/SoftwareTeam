export default function FeedbackSection({ feedback }) {
  const paragraphs = feedback.split(/\n+/).filter(Boolean);
  return (
    <div className="bg-gray-50 border border-gray-200 rounded-xl p-6">
      <h2 className="text-lg font-bold text-gray-800 mb-4">🎤 The Brutal Truth</h2>
      <div className="space-y-3">
        {paragraphs.map((para, i) => (
          <p key={i} className="text-gray-700 leading-relaxed">{para}</p>
        ))}
      </div>
    </div>
  );
}
