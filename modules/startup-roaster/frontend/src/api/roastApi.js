export async function submitRoast(pitch) {
  const res = await fetch('/api/roast', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ pitch }),
  });
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ?? 'Failed to get roast');
  return data;
}

export async function getRoast(id) {
  const res = await fetch(`/api/roast/${id}`);
  const data = await res.json();
  if (!res.ok) throw new Error(data.error ?? 'Roast not found');
  return data;
}
