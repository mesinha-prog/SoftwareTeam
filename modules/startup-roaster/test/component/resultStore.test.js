import { describe, it, expect, beforeEach } from 'vitest';

// Re-import fresh module each test by clearing module cache via dynamic import trick
// We test the store logic directly by importing the module
let save, get;

beforeEach(async () => {
  // Reset module to clear in-memory state between tests
  const mod = await import('../../server/store/resultStore.js?t=' + Date.now());
  save = mod.save;
  get = mod.get;
});

describe('resultStore', () => {
  it('TC-01: save() stores a result and returns a UUID', () => {
    const result = { pitch: 'Uber for cats', score: 2, scoreLabel: 'Pivot Needed ASAP', feedback: 'Meh', suggestions: ['Try harder'] };
    const id = save(result);
    expect(id).toMatch(/^[0-9a-f-]{36}$/);
  });

  it('TC-02: get() retrieves result by valid id', () => {
    const result = { pitch: 'AI for dogs', score: 4, scoreLabel: 'Hidden Gem', feedback: 'Not bad', suggestions: ['Ship it'] };
    const id = save(result);
    const retrieved = get(id);
    expect(retrieved).toMatchObject({ pitch: 'AI for dogs', score: 4 });
    expect(retrieved.id).toBe(id);
  });

  it('TC-03: get() returns null for unknown id', () => {
    expect(get('nonexistent-id')).toBeNull();
  });
});
