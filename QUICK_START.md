# 🚀 Quick Start Checklist — AgriBot Setup

## Day 1: Local Setup & Training (30 minutes - 1 hour)

```bash
# 1. Open PowerShell, navigate to project
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"

# 2. Create virtual environment
python -m venv venv

# 3. Activate virtual environment (Windows)
venv\Scripts\activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Train all models (15-20 minutes)
python run_training.py
# Wait for: "All models trained successfully!"
```

✅ **Result:** Models trained and saved in `models/` folder

---

## Day 1: Create Hugging Face Account (10 minutes)

1. Go to https://huggingface.co/
2. Sign up with email or GitHub
3. Verify email
4. Go to https://huggingface.co/settings/tokens
5. Click "New token"
6. Copy your token (save it somewhere safe)
7. Go to https://huggingface.co/new
8. Create repo: name = `agribot-models`, type = `Model`, visibility = `Public`

✅ **Result:** Your repo will be: `https://huggingface.co/YOUR_USERNAME/agribot-models`

---

## Day 1: Upload Models to Hugging Face (15 minutes)

```bash
# With venv still activated

# 1. Login to Hugging Face
huggingface-cli login
# Paste your token, press Enter

# 2. Upload models (simple!)
python upload_models.py
# Wait for: "✅ Upload complete!"
```

✅ **Result:** All models in Hugging Face Hub

---

## Day 1: Test API Locally (10 minutes)

```bash
# With venv activated

# Start API server
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
# Wait for: "Uvicorn running on http://127.0.0.1:8000"
```

Open in browser: http://localhost:8000/docs

**Test endpoints:**
1. Click "POST /predict/crop" → Try it out
2. Paste:
   ```json
   {
     "N": 90, "P": 42, "K": 43,
     "temperature": 25, "humidity": 80,
     "ph": 6.5, "rainfall": 200, "top_k": 3
   }
   ```
3. Click Execute → ✅ Should see crop recommendations
4. Try other endpoints too!

---

## Day 2: Update API Configuration (5 minutes)

Open: `api/predictor.py`

Find line 9-10:
```python
HF_REPO_ID = "MushiurRahmanAi/AgribotMushiur"
```

Change to YOUR username (from upload output):
```python
HF_REPO_ID = "YOUR_USERNAME/agribot-models"
```

Save file (Ctrl+S)

---

## Day 2: Deploy on Railway (30 minutes)

1. Go to https://railway.app/
2. Sign up / Login with GitHub
3. Click "Create" → "New Project"
4. Click "Deploy from GitHub repo"
5. Select your agribot repo → Deploy

**Wait 2-3 minutes for deployment...**

6. Go to "Variables" tab
7. Add:
   - Key: `HF_REPO_ID`
   - Value: `YOUR_USERNAME/agribot-models`

**Wait for deployment to complete (check in "Deployments" tab)**

8. Copy Railway domain (looks like: `https://agribot-prod-xxxx.up.railway.app`)

✅ **Result:** API running on Railway!

---

## Day 2: Test Railway Backend (5 minutes)

Replace with YOUR Railway domain:

```bash
# Test endpoint
curl https://YOUR-RAILWAY-DOMAIN/health

# Should return: {"status": "ok"}
```

---

## Day 2: Update Frontend (5 minutes)

Open: `frontend/index.html`

Find this line (around line 5):
```javascript
const API_URL = "http://localhost:8000";
```

Change to:
```javascript
const API_URL = "https://YOUR-RAILWAY-DOMAIN";
```

Save file.

---

## Day 3: Deploy Frontend on Netlify (10 minutes)

1. Go to https://netlify.com/
2. Click "Deploy manually" or connect GitHub
3. Drag & drop `frontend/index.html` (or folder)
4. ✅ Netlify will give you a domain like: `https://agribot-xxxx.netlify.app`

---

## Final Test: End-to-End (5 minutes)

1. Open your Netlify frontend URL in browser
2. Send a message: "My rice is yellow"
3. Backend (Railway) → Gets request
4. Backend downloads models from Hugging Face Hub
5. Returns disease diagnosis
6. Frontend shows response

✅ **All done! Full project working!**

---

## 🎯 Summary: What's Where?

| Component | Location | Status |
|-----------|----------|--------|
| **Models** | Hugging Face Hub | ✅ Cloud storage |
| **Backend API** | Railway | ✅ Deployed |
| **Frontend** | Netlify | ✅ Deployed |
| **Local Dev** | Your laptop | ✅ Running |

---

## ⚡ Handy Commands

```bash
# Activate venv (Windows)
venv\Scripts\activate

# Train everything
python run_training.py

# Upload to HF
python upload_models.py

# Start API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# View API docs
http://localhost:8000/docs

# Check local API
curl http://localhost:8000/health

# Check Railway API
curl https://YOUR-RAILWAY-DOMAIN/health
```

---

## 📝 Notes

- **First run slower:** First API call downloads models from HF (~100MB). Subsequent calls use local cache.
- **Private models:** If your HF repo is private, add `HF_TOKEN` environment variable to Railway.
- **GPU training:** Install `torch` with CUDA for faster training: `pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118`

**Questions? Check LOCAL_SETUP_GUIDE.md for detailed troubleshooting!**

