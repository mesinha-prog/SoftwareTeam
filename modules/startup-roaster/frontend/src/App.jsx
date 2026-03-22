import { BrowserRouter, Routes, Route } from 'react-router-dom';
import HomePage from './pages/HomePage';
import ResultPage from './pages/ResultPage';

export default function App() {
  return (
    <BrowserRouter>
      <div className="min-h-screen bg-gradient-to-br from-orange-50 to-amber-50">
        <header className="border-b border-orange-100 bg-white/80 backdrop-blur-sm sticky top-0 z-10">
          <div className="max-w-xl mx-auto px-4 py-3 flex items-center gap-2">
            <span className="text-xl">🔥</span>
            <span className="font-bold text-gray-900">Startup Roaster</span>
            <span className="text-xs text-gray-400 ml-1">brutally honest AI feedback</span>
          </div>
        </header>
        <main>
          <Routes>
            <Route path="/" element={<HomePage />} />
            <Route path="/roast/:id" element={<ResultPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}
