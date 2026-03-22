export default function LoadingSpinner() {
  return (
    <div className="flex flex-col items-center gap-4 py-12">
      <div className="w-14 h-14 border-4 border-orange-300 border-t-orange-600 rounded-full animate-spin" />
      <p className="text-orange-700 font-medium text-lg">Roasting your idea...</p>
      <p className="text-gray-500 text-sm">Consulting our brutally honest AI panel</p>
    </div>
  );
}
