import { Router } from 'express';
import { getRoast } from '../services/claudeService.js';
import { save, get } from '../store/resultStore.js';

const router = Router();

router.post('/', async (req, res) => {
  const { pitch } = req.body;

  if (!pitch || typeof pitch !== 'string' || !pitch.trim()) {
    return res.status(400).json({ error: 'pitch is required' });
  }
  if (pitch.length > 300) {
    return res.status(400).json({ error: 'pitch must be 300 characters or fewer' });
  }

  try {
    const result = await getRoast(pitch.trim());
    const id = save({ pitch: pitch.trim(), ...result });
    res.status(201).json({ id, pitch: pitch.trim(), ...result });
  } catch (err) {
    console.error('Roast error:', err.message);
    res.status(500).json({ error: 'Failed to generate roast. Please try again.' });
  }
});

router.get('/:id', (req, res) => {
  const result = get(req.params.id);
  if (!result) {
    return res.status(404).json({ error: 'Roast not found' });
  }
  res.json(result);
});

export default router;
