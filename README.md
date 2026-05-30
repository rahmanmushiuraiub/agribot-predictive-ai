# 🌱 AgriBot — English-Language Agricultural Advisory Chatbot

NLP course project. Combines **BERT (DistilBERT)** intent classification with
**scikit-learn** ML models served via **FastAPI**.

---

## 📁 Project Structure

```
agribot/
├── data/                                   # Raw datasets (CSV)
│   ├── Crop_recommendation.csv
│   ├── Fertilizer Prediction.csv
│   └── Crop Recommendation using Soil Properties and Weather Prediction.csv
│
├── training/                               # Model training scripts
│   ├── train_crop_model.py                 # Ensemble crop classifier
│   ├── train_fertilizer_model.py           # Fertilizer RandomForest
│   └── train_intent_classifier.py          # Fine-tune DistilBERT
│
├── models/                                 # Saved model files (auto-generated)
│   ├── crop_model.pkl
│   ├── crop_label_encoder.pkl
│   ├── crop_scaler.pkl
│   ├── crop_meta.json
│   ├── fertilizer_model.pkl
│   ├── fertilizer_encoders.pkl
│   ├── fertilizer_scaler.pkl
│   ├── fertilizer_meta.json
│   └── intent_model/                       # HuggingFace DistilBERT
│
├── api/
│   ├── main.py                             # FastAPI app (all routes)
│   ├── predictor.py                        # Model loading & inference
│   └── chatbot.py                          # Response generation + disease KB
│
├── frontend/
│   └── index.html                          # Standalone chatbot UI
│
├── run_training.py                         # Run all training in sequence
└── requirements.txt
```

---

## ⚙️ Setup (Google Colab / Local)

### Step 1 — Install dependencies

```bash
pip install -r requirements.txt
```

> **Google Colab tip:** Run `!pip install -r requirements.txt` in a cell.

### Step 2 — Place datasets

Make sure all 3 CSV files are in the `data/` folder:
- `Crop_recommendation.csv`
- `Fertilizer Prediction.csv`
- `Crop Recommendation using Soil Properties and Weather Prediction.csv`

---

## 🏋️ Training the Models

### Option A — Run all at once

```bash
python run_training.py
```

### Option B — Run individually

```bash
# 1. Crop recommendation (sklearn ensemble)
python training/train_crop_model.py

# 2. Fertilizer prediction (RandomForest)
python training/train_fertilizer_model.py

# 3. BERT intent classifier (DistilBERT fine-tuning)
python training/train_intent_classifier.py
```

Training times (CPU):
- Crop model:       ~1–2 min
- Fertilizer model: ~2–4 min
- BERT model:       ~5–10 min (GPU recommended)

All saved model files appear in `models/`.

---

## 🚀 Running the API Server

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Open your browser: **http://127.0.0.1:8000/docs** → Interactive Swagger UI

### Key Endpoints

| Method | URL                    | Description                        |
|--------|------------------------|------------------------------------|
| GET    | `/`                    | Health check                       |
| GET    | `/ui`                  | Chatbot frontend                   |
| GET    | `/meta/crops`          | Available crop classes             |
| GET    | `/meta/fertilizers`    | Available fertilizer info          |
| POST   | `/predict/crop`        | Crop recommendation (JSON body)    |
| POST   | `/predict/fertilizer`  | Fertilizer recommendation          |
| POST   | `/chat`                | Main chat endpoint                 |

### Example: `/chat` request

```bash
curl -X POST http://127.0.0.1:8000/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Recommend a crop: N=90, P=42, K=43, temp=25, humidity=80, pH=6.5, rainfall=200"}'
```

Response:
```json
{
  "intent":     "crop_recommendation",
  "confidence": 0.97,
  "response":   "🌾 Crop Recommendations ...",
  "data":       { "top_recommendations": [...] }
}
```

### Example: `/predict/crop`

```bash
curl -X POST http://127.0.0.1:8000/predict/crop \
  -H "Content-Type: application/json" \
  -d '{"N":90,"P":42,"K":43,"temperature":25,"humidity":80,"ph":6.5,"rainfall":200,"top_k":3}'
```

### Example: `/predict/fertilizer`

```bash
curl -X POST http://127.0.0.1:8000/predict/fertilizer \
  -H "Content-Type: application/json" \
  -d '{"temperature":32,"humidity":51,"moisture":41,"soil_type":"Sandy","crop_type":"Wheat","nitrogen":10,"potassium":5,"phosphorous":15,"top_k":3}'
```

---

## 🌐 Connecting the Frontend

Open `frontend/index.html` directly in any browser.

The frontend sends requests to `http://127.0.0.1:8000`. To change the server URL,
edit this line in `index.html`:

```javascript
const API_BASE = "http://127.0.0.1:8000";  // ← Change to your deployed URL
```

### Deploying to a Web Server

1. **Deploy API** to any cloud (Render, Railway, Heroku, AWS EC2):
   ```bash
   uvicorn api.main:app --host 0.0.0.0 --port $PORT
   ```

2. **Update `API_BASE`** in `index.html` to your deployed URL, e.g.:
   ```javascript
   const API_BASE = "https://agribot.onrender.com";
   ```

3. **Host frontend** on GitHub Pages, Netlify, or Vercel (just upload `frontend/index.html`).

---

## 🤖 How It Works

```
Farmer types a message
        ↓
  DistilBERT Intent Classifier
        ↓
  ┌─────────────────────────────────┐
  │ crop_recommendation             │→ Ensemble Model (RF + GB) → top-3 crops
  │ fertilizer_advice               │→ RandomForest → top-3 fertilizers
  │ crop_disease                    │→ Disease Knowledge Base → diagnosis
  │ weather_planting                │→ Rule-based advisor
  └─────────────────────────────────┘
        ↓
  Natural language response → Farmer
```

---

## 📊 Datasets Used

| Dataset | Source | Records | Task |
|---------|--------|---------|------|
| Crop_recommendation.csv | Kaggle | 2,200 | Crop classification |
| Fertilizer Prediction.csv | Kaggle | 100,000 | Fertilizer classification |
| Soil+Weather Prediction.csv | Mendeley (NASA+ATA) | varies | Crop classification |

---

## 🔧 Extending the Project

- **Add more disease rules:** Edit `DISEASE_KB` in `api/chatbot.py`
- **Add real weather data:** Integrate OpenWeatherMap API in `api/chatbot.py`
- **More intents:** Add sentences to `TRAINING_DATA` in `train_intent_classifier.py`
- **Swap to full BERT:** Change `distilbert-base-uncased` → `bert-base-uncased` in training script
