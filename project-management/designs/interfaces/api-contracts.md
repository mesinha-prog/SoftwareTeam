# Interface Specifications: Startup Idea Roaster

## REST API Contracts

### POST /api/roast

Submit a startup pitch for AI roasting.

**Request Headers**: `Content-Type: application/json`

**Request Body**:
```json
{
  "pitch": "string"
}
```
- `pitch`: Required. 1–300 characters. The user's startup idea description.

**Success Response** (HTTP 201):
```json
{
  "id": "550e8400-e29b-41d4-a716-446655440000",
  "pitch": "Uber for dogs but make it blockchain",
  "score": 1,
  "scoreLabel": "Certified Dumpster Fire",
  "feedback": "Let's start with the blockchain part...",
  "suggestions": [
    "Drop the blockchain — it adds zero value here",
    "Talk to 20 dog owners before writing a line of code",
    "Find a specific pain point: grooming? vet trips? walks?"
  ]
}
```

**Error Responses**:
| Status | Reason |
|--------|--------|
| 400 | Missing pitch, pitch too long (>300 chars), or pitch is not a string |
| 500 | Claude API call failed or returned invalid JSON |

---

### GET /api/roast/:id

Retrieve a previously generated roast result by ID.

**Path Parameter**: `id` — UUID v4 string

**Success Response** (HTTP 200): Same shape as POST response above.

**Error Responses**:
| Status | Reason |
|--------|--------|
| 404 | No result found for this ID |

---

## Claude API Prompt Contract

### System Prompt

```
You are a brutally honest startup idea critic. Your job is to roast startup ideas with a mix of savage sarcasm and real constructive criticism.

Score the idea on this scale:
1 = "Certified Dumpster Fire" (fundamentally broken)
2 = "Pivot Needed ASAP" (core issues, major changes needed)
3 = "Meh But Possible" (average, needs differentiation)
4 = "Hidden Gem" (strong potential, needs polish)
5 = "Future Unicorn" (exceptional idea, strong execution path)

Respond ONLY with valid JSON. No markdown, no preamble, no explanation outside the JSON.

Required JSON format:
{
  "score": <integer 1-5>,
  "scoreLabel": "<exact label from the scale above>",
  "feedback": "<2-4 paragraphs of brutal honest feedback combining sarcasm and real critique>",
  "suggestions": ["<3-5 specific fix-it suggestions mixing tactical actions and strategic advice>"]
}
```

### User Message Format

```
Startup idea: {pitch}
```

### Expected Claude Response

Strictly valid JSON matching the schema above. The backend must:
1. Parse the JSON response
2. Validate `score` is integer 1–5
3. Validate `scoreLabel` matches one of the 5 defined labels
4. Return 500 if parsing or validation fails

---

## Frontend ↔ Backend Contract (roastApi.js)

```javascript
// Submit a pitch — returns { id, score, scoreLabel, feedback, suggestions, pitch }
submitRoast(pitch: string): Promise<RoastResult>

// Fetch existing roast by ID — returns same RoastResult shape
getRoast(id: string): Promise<RoastResult>
```

### RoastResult type

```typescript
interface RoastResult {
  id: string;
  pitch: string;
  score: 1 | 2 | 3 | 4 | 5;
  scoreLabel: "Certified Dumpster Fire" | "Pivot Needed ASAP" | "Meh But Possible" | "Hidden Gem" | "Future Unicorn";
  feedback: string;
  suggestions: string[];
}
```
