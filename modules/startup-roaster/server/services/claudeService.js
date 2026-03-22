import Anthropic from '@anthropic-ai/sdk';

const VALID_LABELS = [
  'Certified Dumpster Fire',
  'Pivot Needed ASAP',
  'Meh But Possible',
  'Hidden Gem',
  'Future Unicorn',
];

const SYSTEM_PROMPT = `You are a brutally honest startup idea critic. Your job is to roast startup ideas with a mix of savage sarcasm and real constructive criticism.

Score the idea on this scale:
1 = "Certified Dumpster Fire" (fundamentally broken — bad idea, bad timing, bad everything)
2 = "Pivot Needed ASAP" (core issues exist, but it's salvageable with major changes)
3 = "Meh But Possible" (average idea, needs real differentiation to survive)
4 = "Hidden Gem" (strong potential, just needs polish and execution)
5 = "Future Unicorn" (exceptional idea with a clear path to massive success)

Be brutal but fair. Mix sarcasm with real hard truths. The feedback should sting a little but also genuinely help.

Respond ONLY with valid JSON. No markdown, no preamble, no explanation outside the JSON.

Required JSON format:
{
  "score": <integer 1-5>,
  "scoreLabel": "<exact label from the scale above>",
  "feedback": "<2-4 paragraphs of brutal honest feedback combining sarcasm and real critique>",
  "suggestions": ["<3-5 specific fix-it suggestions mixing tactical actions and strategic advice>"]
}`;

const client = new Anthropic();

export async function getRoast(pitch) {
  const message = await client.messages.create({
    model: 'claude-sonnet-4-6',
    max_tokens: 1024,
    system: SYSTEM_PROMPT,
    messages: [{ role: 'user', content: `Startup idea: ${pitch}` }],
  });

  const text = message.content[0].text.trim();
  let parsed;
  try {
    parsed = JSON.parse(text);
  } catch {
    throw new Error('Claude returned non-JSON response');
  }

  const { score, scoreLabel, feedback, suggestions } = parsed;

  if (!Number.isInteger(score) || score < 1 || score > 5) {
    throw new Error(`Invalid score value: ${score}`);
  }
  if (!VALID_LABELS.includes(scoreLabel)) {
    throw new Error(`Invalid scoreLabel: ${scoreLabel}`);
  }
  if (typeof feedback !== 'string' || !feedback.trim()) {
    throw new Error('Missing feedback');
  }
  if (!Array.isArray(suggestions) || suggestions.length === 0) {
    throw new Error('Missing suggestions');
  }

  return { score, scoreLabel, feedback, suggestions };
}
