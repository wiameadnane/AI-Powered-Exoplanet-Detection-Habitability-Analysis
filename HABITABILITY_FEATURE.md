# 🌍 Habitability Analysis Feature

## Overview

When an exoplanet is detected, the system automatically analyzes its habitability by comparing it to Earth using AI (GPT-4). This provides insights into how suitable the planet might be for life.

---

## How It Works

### 1. **Exoplanet Detection**
   - User submits observation data (40 features)
   - XGBoost model predicts: Exoplanet or Not
   - If exoplanet detected → proceed to habitability analysis

### 2. **Habitability Analysis (LLM)**
   - Extracts key features:
     - Orbital Period (pl_orbper)
     - Planet Radius (pl_rade)
     - Insolation Flux (pl_insol)
     - Equilibrium Temperature (pl_eqt)
     - Stellar Effective Temperature (st_teff)
     - Stellar Radius (st_rad)
     - Stellar Surface Gravity (st_logg)
   
   - Compares to Earth reference values
   - Uses GPT-4 to analyze habitability
   - Returns percentage (0-100%) and explanation

### 3. **Display Results**
   - Habitability score with visual icon
   - Progress bar showing Earth similarity
   - Detailed explanation from AI

---

## Earth Reference Values

The AI compares detected exoplanets against these Earth values:

| Property | Earth Value |
|----------|-------------|
| Orbital Period | 365.256 days |
| Planet Radius | 1.0 R_earth |
| Insolation Flux | 1.0 Earth flux |
| Equilibrium Temperature | 255 K |
| Stellar Effective Temperature | 5772 K |
| Stellar Radius | 1.0 R_sun |
| Stellar Surface Gravity | 4.44 dex |

---

## Habitability Score Interpretation

| Score | Icon | Category | Description |
|-------|------|----------|-------------|
| 70-100% | 🌍 | Highly Habitable | Very Earth-like conditions |
| 50-70% | 🌿 | Potentially Habitable | Some Earth-like qualities |
| 30-50% | 🪨 | Marginally Habitable | Challenging conditions |
| 0-30% | ❄️ | Unlikely Habitable | Extreme conditions |

---

## API Endpoints

### Combined Detection + Habitability
```http
POST /api/predict
Content-Type: application/json

{
  "ra": 112.357708,
  "dec": -12.69596,
  ... (all 40 features)
}
```

**Response (if exoplanet detected):**
```json
{
  "prediction": 1,
  "is_exoplanet": true,
  "confidence": 0.9168,
  "probabilities": {
    "not_exoplanet": 0.0832,
    "exoplanet": 0.9168
  },
  "label": "Exoplanet Detected! 🌟",
  "habitability": {
    "success": true,
    "habitability_score": 45.5,
    "explanation": "This exoplanet shows moderate habitability..."
  }
}
```

### Standalone Habitability Analysis
```http
POST /api/habitability
Content-Type: application/json

{
  "pl_orbper": 365.25,
  "pl_rade": 1.2,
  "pl_insol": 0.9,
  "pl_eqt": 260,
  "st_teff": 5800,
  "st_rad": 1.1,
  "st_logg": 4.4
}
```

---

## Setup Requirements

### 1. Environment Variable
Create/update `.env` file:
```env
OPENROUTER_API_KEY=sk-or-v1-your-api-key-here
```

### 2. Install Dependencies
```bash
pip install openai python-dotenv
```

Or:
```bash
pip install -r requirements.txt
```

### 3. Verify Setup
```bash
python test_env.py
```

Expected output:
```
✅ OPENROUTER_API_KEY is loaded!
```

---

## Testing

### Test Habitability Feature
```bash
python test_habitability.py
```

This will:
1. Check if LLM is enabled
2. Load example data
3. Detect exoplanet
4. Analyze habitability
5. Display results

### Manual Test via Browser
1. Go to http://localhost:5000
2. Click "Load Example"
3. Click "Detect Exoplanet"
4. Wait for detection results
5. View habitability analysis below (if exoplanet detected)

---

## Example Output

```
🎉 DETECTION RESULTS
======================================================================
Result: Exoplanet Detected! 🌟
Confidence: 91.68%

🌍 HABITABILITY ANALYSIS
======================================================================
Habitability Score: 45.5% Earth similarity
Category: 🪨 Marginally Habitable

Explanation:
----------------------------------------------------------------------
This exoplanet shows moderate habitability potential. The equilibrium
temperature of 3127K is significantly higher than Earth's 255K,
indicating extreme surface temperatures. However, the planet radius
of 5.8 Earth radii suggests it may be a gas giant rather than rocky.
The high insolation flux would make surface conditions challenging
for Earth-like life, though subsurface or atmospheric life cannot
be ruled out...
```

---

## Cost Considerations

- Each habitability analysis makes 1 API call to OpenRouter
- Using model: `openai/gpt-4o-mini` (cost-effective)
- Typical token usage: ~400 tokens per analysis
- Only triggered when exoplanet is detected

**Tip:** For testing, use the `/api/health` endpoint to verify LLM is enabled before making predictions.

---

## Troubleshooting

### LLM Not Available
```json
{
  "habitability": {
    "error": "LLM not available",
    "explanation": "Habitability analysis requires OpenAI API key"
  }
}
```

**Fix:** Set `OPENROUTER_API_KEY` in `.env` file

### API Key Invalid
```json
{
  "habitability": {
    "success": false,
    "error": "Unauthorized",
    "explanation": "Error analyzing habitability: Unauthorized"
  }
}
```

**Fix:** Verify your API key is correct

### Model Not Found
**Fix:** Check if `openai/gpt-4o-mini` is available, or change model in `app.py` line 259

---

## Customization

### Change AI Model
Edit `app.py` line 259:
```python
model="openai/gpt-4o-mini",  # Change to your preferred model
```

### Adjust Response Length
Edit `app.py` line 264:
```python
max_tokens=500  # Increase for longer explanations
```

### Modify Prompt
Edit the prompt in `app.py` lines 236-256 to customize analysis criteria

---

## Privacy & Security

- ✅ API key stored in `.env` (not in code)
- ✅ `.env` excluded from git via `.gitignore`
- ✅ Only 7 planet features sent to AI (not raw observation data)
- ✅ No user data or location information shared

---

## Credits

- **AI Model:** GPT-4 via OpenRouter
- **Science:** NASA Exoplanet Archive data
- **Detection:** XGBoost ML model (95.34% AUC)

---

**Enjoy discovering habitable worlds! 🌍🚀**
