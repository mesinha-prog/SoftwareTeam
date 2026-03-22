import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import PitchForm from '../components/PitchForm';
import LoadingSpinner from '../components/LoadingSpinner';
import { submitRoast } from '../api/roastApi';

export default function HomePage() {
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleSubmit = async (pitch) => {
    setIsLoading(true);
    setError(null);
    try {
      const result = await submitRoast(pitch);
      navigate(`/roast/${result.id}`);
    } catch (err) {
      setError(err.message);
      setIsLoading(false);
    }
  };

  return (
    <div className="max-w-xl mx-auto py-12 px-4">
      <div className="text-center mb-10">
        <div className="text-6xl mb-4">🔥</div>
        <h1 className="text-4xl font-extrabold text-gray-900 mb-2">Startup Roaster</h1>
        <p className="text-gray-500 text-lg">Brutally honest AI feedback on your startup idea</p>
      </div>

      {isLoading ? (
        <LoadingSpinner />
      ) : (
        <>
          <PitchForm onSubmit={handleSubmit} isLoading={isLoading} />
          {error && (
            <div className="mt-4 p-4 bg-red-50 border border-red-200 rounded-xl text-red-700 text-sm">
              {error}
            </div>
          )}
        </>
      )}
    </div>
  );
}
