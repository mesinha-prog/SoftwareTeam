import { useEffect, useState } from 'react';
import { useParams, Link } from 'react-router-dom';
import RoastScore from '../components/RoastScore';
import FeedbackSection from '../components/FeedbackSection';
import SuggestionsSection from '../components/SuggestionsSection';
import ShareButton from '../components/ShareButton';
import LoadingSpinner from '../components/LoadingSpinner';
import { getRoast } from '../api/roastApi';

export default function ResultPage() {
  const { id } = useParams();
  const [result, setResult] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    getRoast(id)
      .then(setResult)
      .catch((err) => setError(err.message));
  }, [id]);

  if (error) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4 text-center">
        <div className="text-5xl mb-4">😕</div>
        <h2 className="text-xl font-bold text-gray-800 mb-2">Roast not found</h2>
        <p className="text-gray-500 mb-6">{error}</p>
        <Link to="/" className="text-orange-500 hover:underline font-medium">← Roast another idea</Link>
      </div>
    );
  }

  if (!result) {
    return (
      <div className="max-w-xl mx-auto py-12 px-4">
        <LoadingSpinner />
      </div>
    );
  }

  return (
    <div className="max-w-xl mx-auto py-10 px-4 space-y-6">
      <div className="text-center">
        <p className="text-gray-500 text-sm mb-1">Your idea</p>
        <p className="text-gray-800 font-medium italic">"{result.pitch}"</p>
      </div>

      <div className="flex justify-center">
        <RoastScore score={result.score} scoreLabel={result.scoreLabel} />
      </div>

      <FeedbackSection feedback={result.feedback} />
      <SuggestionsSection suggestions={result.suggestions} />

      <div className="flex items-center justify-between pt-2">
        <ShareButton />
        <Link to="/" className="text-orange-500 hover:underline font-medium text-sm">
          ← Roast another idea
        </Link>
      </div>
    </div>
  );
}
