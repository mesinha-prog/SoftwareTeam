import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import '@testing-library/jest-dom';
import PitchForm from '../components/PitchForm';
import RoastScore from '../components/RoastScore';
import ShareButton from '../components/ShareButton';

// TC-10: PitchForm renders
describe('PitchForm', () => {
  it('TC-10: renders textarea and submit button', () => {
    render(<PitchForm onSubmit={() => {}} isLoading={false} />);
    expect(screen.getByRole('textbox')).toBeInTheDocument();
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('TC-11: button is disabled when input is empty', () => {
    render(<PitchForm onSubmit={() => {}} isLoading={false} />);
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('TC-12: button is disabled when input exceeds 300 chars', () => {
    render(<PitchForm onSubmit={() => {}} isLoading={false} />);
    const textarea = screen.getByRole('textbox');
    fireEvent.change(textarea, { target: { value: 'A'.repeat(301) } });
    expect(screen.getByRole('button')).toBeDisabled();
  });

  it('TC-13: shows character counter', () => {
    render(<PitchForm onSubmit={() => {}} isLoading={false} />);
    expect(screen.getByText('300')).toBeInTheDocument();
  });

  it('button is enabled with valid input', () => {
    const onSubmit = vi.fn();
    render(<PitchForm onSubmit={onSubmit} isLoading={false} />);
    const textarea = screen.getByRole('textbox');
    fireEvent.change(textarea, { target: { value: 'Airbnb for parking spaces' } });
    expect(screen.getByRole('button')).not.toBeDisabled();
  });
});

// TC-14: RoastScore renders all 5 score levels
describe('RoastScore', () => {
  const scores = [
    { score: 1, scoreLabel: 'Certified Dumpster Fire', emoji: '💀' },
    { score: 2, scoreLabel: 'Pivot Needed ASAP', emoji: '🔥' },
    { score: 3, scoreLabel: 'Meh But Possible', emoji: '😐' },
    { score: 4, scoreLabel: 'Hidden Gem', emoji: '💎' },
    { score: 5, scoreLabel: 'Future Unicorn', emoji: '🦄' },
  ];

  scores.forEach(({ score, scoreLabel, emoji }) => {
    it(`TC-14: score ${score} shows "${scoreLabel}" and ${emoji}`, () => {
      render(<RoastScore score={score} scoreLabel={scoreLabel} />);
      expect(screen.getByText(scoreLabel)).toBeInTheDocument();
      expect(screen.getByText(emoji)).toBeInTheDocument();
    });
  });
});

// TC-15: ShareButton copies URL
describe('ShareButton', () => {
  it('TC-15: renders share button', () => {
    render(<ShareButton />);
    expect(screen.getByRole('button')).toBeInTheDocument();
  });

  it('TC-15: shows copied feedback after click', async () => {
    Object.assign(navigator, {
      clipboard: { writeText: vi.fn().mockResolvedValue(undefined) },
    });
    render(<ShareButton />);
    fireEvent.click(screen.getByRole('button'));
    expect(await screen.findByText('✅ Link Copied!')).toBeInTheDocument();
  });
});
