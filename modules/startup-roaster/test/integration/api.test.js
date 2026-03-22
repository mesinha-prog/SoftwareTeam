import { describe, it, expect, vi, beforeAll } from 'vitest';
import express from 'express';
import supertest from 'supertest';
import cors from 'cors';

// Mock claudeService before importing routes
vi.mock('../../server/services/claudeService.js', () => ({
  getRoast: vi.fn(async (pitch) => ({
    score: 3,
    scoreLabel: 'Meh But Possible',
    feedback: 'Your idea is as original as a plain bagel.',
    suggestions: ['Narrow your ICP', 'Talk to 20 customers first', 'Drop the blockchain'],
  })),
}));

let app;
let request;

beforeAll(async () => {
  app = express();
  app.use(cors());
  app.use(express.json());
  const { default: roastRouter } = await import('../../server/routes/roast.js');
  app.use('/api/roast', roastRouter);
  request = supertest(app);
});

describe('POST /api/roast', () => {
  it('TC-04: valid pitch returns 201 with full result and id', async () => {
    const res = await request.post('/api/roast').send({ pitch: 'Airbnb for parking spaces' });
    expect(res.status).toBe(201);
    expect(res.body.id).toMatch(/^[0-9a-f-]{36}$/);
    expect(res.body.score).toBe(3);
    expect(res.body.scoreLabel).toBe('Meh But Possible');
    expect(res.body.feedback).toBeTruthy();
    expect(Array.isArray(res.body.suggestions)).toBe(true);
    expect(res.body.pitch).toBe('Airbnb for parking spaces');
  });

  it('TC-05: missing pitch returns 400', async () => {
    const res = await request.post('/api/roast').send({});
    expect(res.status).toBe(400);
  });

  it('TC-06: empty pitch returns 400', async () => {
    const res = await request.post('/api/roast').send({ pitch: '   ' });
    expect(res.status).toBe(400);
  });

  it('TC-07: pitch over 300 chars returns 400', async () => {
    const longPitch = 'A'.repeat(301);
    const res = await request.post('/api/roast').send({ pitch: longPitch });
    expect(res.status).toBe(400);
  });
});

describe('GET /api/roast/:id', () => {
  it('TC-08: valid id returns 200 with result', async () => {
    // First create a roast
    const postRes = await request.post('/api/roast').send({ pitch: 'Tinder for pets' });
    const { id } = postRes.body;

    const res = await request.get(`/api/roast/${id}`);
    expect(res.status).toBe(200);
    expect(res.body.id).toBe(id);
    expect(res.body.pitch).toBe('Tinder for pets');
  });

  it('TC-09: unknown id returns 404', async () => {
    const res = await request.get('/api/roast/00000000-0000-0000-0000-000000000000');
    expect(res.status).toBe(404);
  });
});
