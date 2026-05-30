# 🌱 AgriBot — Complete Local Setup & Deployment Guide

Complete guide to train models locally, upload to Hugging Face, deploy on Railway, and run the project end-to-end.

---

## 📋 Overview of Steps

1. **Setup Local Environment**
2. **Train Models Locally**
3. **Create Hugging Face Account & Repository**
4. **Upload Models to Hugging Face Hub**
5. **Configure Railway Backend**
6. **Test Locally**
7. **Deploy to Production**

---

## ✅ Step 1: Setup Local Environment

### 1.1 Install Python (if not already installed)
- Download Python 3.9+ from https://www.python.org/downloads/
- Make sure to check "Add Python to PATH" during installation

### 1.2 Create a Virtual Environment
```bash
# Navigate to your project folder
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"

# Create virtual environment
python -m venv venv

# Activate it
# On Windows:
venv\Scripts\activate
# On Mac/Linux:
source venv/bin/activate
```

### 1.3 Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

**Expected output:** All packages installed successfully (no errors)

---

## 🏋️ Step 2: Train Models Locally

### 2.1 Verify Data Files
Make sure these CSV files exist in `data/` folder:
- ✅ `Crop_recommendation.csv`
- ✅ `Fertilizer Prediction.csv`
- ✅ `Crop Recommendation using Soil Properties and Weather Prediction.csv`

### 2.2 Run Training (Option A: Train All Models at Once)

```bash
# From project root (with venv activated)
python run_training.py
```

**Expected output:**
```
Starting crop model training...
Crop model trained and saved!
Starting fertilizer model training...
Fertilizer model trained and saved!
Starting intent classifier training...
Intent classifier trained and saved!
All models trained successfully!
```

⏱️ **Total time:** ~15-20 minutes (depends on CPU/GPU)

### 2.2 Alternative: Train Individual Models

```bash
# 1. Train crop prediction model (~2 min)
python training/train_crop_model.py

# 2. Train fertilizer model (~3 min)
python training/train_fertilizer_model.py

# 3. Train intent classifier (~5-10 min, faster with GPU)
python training/train_intent_classifier.py
```

### 2.3 Verify Models Were Created
Check `models/` folder for:
- ✅ `crop_model.pkl` and related files
- ✅ `fertilizer_model.pkl` and related files
- ✅ `intent_model/` folder with BERT files

---

## 🤗 Step 3: Create Hugging Face Account & Repository

### 3.1 Create Hugging Face Account
1. Go to https://huggingface.co/
2. Click "Sign Up"
3. Complete registration
4. Verify your email

### 3.2 Create Your API Token
1. Go to https://huggingface.co/settings/tokens
2. Click "New token"
3. Name: `agribot-models` (optional)
4. Role: `write` (allows uploads)
5. Copy the token (you'll need it soon)

### 3.3 Create Model Repository
1. Go to https://huggingface.co/new
2. Fill in:
   - **Repository name:** `agribot-models`
   - **Repository type:** Model
   - **Visibility:** Public (or Private if you prefer)
3. Click "Create repository"

**Your repo will be:** `https://huggingface.co/{YOUR_USERNAME}/agribot-models`

---

## 📦 Step 4: Upload Models to Hugging Face Hub

### 4.1 Login to Hugging Face
```bash
# With venv activated
huggingface-cli login
# Paste your API token when prompted, then press Enter
```

### 4.2 Option A: Upload Using Python Script (Recommended)

Create a file `upload_models.py` in your project root:

```python
from huggingface_hub import HfApi, HfFolder

# Get your HuggingFace username
api = HfApi()
user_info = api.whoami()
username = user_info['name']
repo_id = f"{username}/agribot-models"

print(f"Uploading to: {repo_id}")

# List of model files to upload
model_files = [
    "models/crop_model.pkl",
    "models/crop_label_encoder.pkl",
    "models/crop_scaler.pkl",
    "models/crop_meta.json",
    "models/fertilizer_model.pkl",
    "models/fertilizer_encoders.pkl",
    "models/fertilizer_scaler.pkl",
    "models/fertilizer_meta.json",
    "models/crop_stats.json",
    "models/yield_meta.json",
    "models/state_profiles.json",
]

# Upload individual files
for file_path in model_files:
    try:
        print(f"Uploading {file_path}...")
        api.upload_file(
            path_or_fileobj=file_path,
            path_in_repo=file_path.split("/")[-1],  # Just filename
            repo_id=repo_id,
            commit_message=f"Upload {file_path.split('/')[-1]}"
        )
        print(f"✅ {file_path} uploaded!")
    except Exception as e:
        print(f"❌ Error uploading {file_path}: {e}")

# Upload intent model folder
print("\nUploading intent_model folder...")
try:
    api.upload_folder(
        folder_path="models/intent_model",
        repo_id=repo_id,
        path_in_repo="intent_model",
        commit_message="Upload BERT intent classifier"
    )
    print("✅ intent_model folder uploaded!")
except Exception as e:
    print(f"❌ Error uploading intent_model: {e}")

print(f"\n✅ All models uploaded! Repository: https://huggingface.co/{repo_id}")
```

Run it:
```bash
python upload_models.py
```

### 4.2 Option B: Upload Using Git (Alternative, Faster)

```bash
# Clone your HF repo
git clone https://huggingface.co/{YOUR_USERNAME}/agribot-models
cd agribot-models

# Copy model files here
cp -r ../agribot_v4/models/* .

# Push to HF
git add .
git commit -m "Upload trained models"
git push
```

---

## 🔧 Step 5: Update API Configuration

### 5.1 Update `api/predictor.py`

Change the HF_REPO_ID to your username:

```python
# Line 9-10, change to:
HF_REPO_ID = "{YOUR_USERNAME}/agribot-models"  # Your repo
HF_CACHE_DIR = os.path.expanduser("~/.cache/agribot_models")
```

Example:
```python
HF_REPO_ID = "john_doe/agribot-models"  # If your username is john_doe
```

---

## 🚀 Step 6: Test API Locally

### 6.1 Start the API Server
```bash
# With venv activated, from project root
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

**Expected output:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

### 6.2 Test in Browser
Open: http://localhost:8000/docs

You'll see interactive API documentation. Try:

**Test Crop Prediction:**
1. Click "POST /predict/crop"
2. Click "Try it out"
3. Enter example values:
   ```json
   {
     "N": 90,
     "P": 42,
     "K": 43,
     "temperature": 25,
     "humidity": 80,
     "ph": 6.5,
     "rainfall": 200,
     "top_k": 3
   }
   ```
4. Click "Execute"
5. ✅ Should return crop recommendations

**Test Chat:**
1. Click "POST /chat"
2. Click "Try it out"
3. Enter: `{"message": "My rice leaves are turning yellow"}`
4. Click "Execute"
5. ✅ Should return disease diagnosis

### 6.3 Test Frontend Locally
1. Open `frontend/index.html` in your browser
2. Send a chat message
3. ✅ Should get responses from localhost:8000

---

## 🚂 Step 7: Deploy on Railway

### 7.1 Create Railway Account
1. Go to https://railway.app/
2. Sign up with GitHub account
3. Create new project

### 7.2 Connect GitHub Repository
1. Click "Create" → "From GitHub repo"
2. Select your AgriBot repository
3. Click "Deploy"

### 7.3 Add Environment Variables
1. In Railway dashboard, go to your project
2. Click "Variables" tab
3. Add these variables:

| Key | Value |
|-----|-------|
| `HF_REPO_ID` | `{YOUR_USERNAME}/agribot-models` |
| `PORT` | `8000` |

### 7.4 Configure Start Command (if needed)

Check Railway's "Settings" tab and ensure Procfile or start command is:

```bash
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### 7.5 Get Your Railway URL
Once deployed:
- Go to "Deployments" tab
- Click the domain to see your API URL
- Example: `https://agribot-production.up.railway.app`

---

## 🔗 Step 8: Update Frontend to Use Railway API

Edit `frontend/index.html`:

Find the API_URL line and change it to your Railway domain:

```javascript
const API_URL = "https://agribot-production.up.railway.app";  // Your Railway URL
```

---

## ✅ Final Verification Checklist

- ✅ Models trained locally
- ✅ Models uploaded to Hugging Face
- ✅ `api/predictor.py` updated with your HF repo ID
- ✅ API tested locally at `localhost:8000/docs`
- ✅ Frontend tested locally (opens index.html and works)
- ✅ Backend deployed on Railway
- ✅ Frontend deployed on Netlify (already done)
- ✅ Frontend updated with Railway API URL
- ✅ Test end-to-end: Netlify frontend → Railway backend → HF Hub models

---

## 🆘 Troubleshooting

### Problem: "ModuleNotFoundError: No module named 'transformers'"
**Solution:**
```bash
pip install --upgrade transformers torch
```

### Problem: Models not downloading from Hugging Face
**Solution:**
```bash
huggingface-cli login  # Re-login
rm -rf ~/.cache/agribot_models  # Clear cache
# Then restart your API
```

### Problem: "models/intent_model" not found
**Solution:**
Train the intent classifier first:
```bash
python training/train_intent_classifier.py
```

### Problem: Railway deployment fails
**Solution:**
1. Check logs in Railway dashboard
2. Verify `requirements.txt` has all dependencies
3. Verify HF_REPO_ID is correct and public

### Problem: "Hugging Face token is invalid"
**Solution:**
```bash
huggingface-cli logout
huggingface-cli login
# Get new token from https://huggingface.co/settings/tokens
```

---

## 📞 Quick Command Reference

```bash
# Activate venv (Windows)
venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Train all models
python run_training.py

# Login to Hugging Face
huggingface-cli login

# Upload models
python upload_models.py

# Test API locally
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

# View API docs
http://localhost:8000/docs
```

---

**You're all set! 🎉 Your AgriBot is ready for local development and production deployment.**

