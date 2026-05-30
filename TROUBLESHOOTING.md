# 🔧 Troubleshooting Guide — AgriBot

## Common Issues & Solutions

---

## ❌ "venv not found" / Can't activate virtual environment

**Error:** `The term 'venv' is not recognized` or `No module named venv`

**Solutions:**
```bash
# Make sure you're in the project directory
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"

# Create venv again
python -m venv venv

# Activate with full path
.\venv\Scripts\activate

# If still not working, try:
python -m venv .venv
.\.venv\Scripts\activate
```

---

## ❌ "ModuleNotFoundError: No module named 'transformers'"

**Error:** When running training or API

**Solution:**
```bash
# Ensure venv is activated
venv\Scripts\activate

# Reinstall requirements
pip install --upgrade pip
pip install -r requirements.txt

# If still fails, install individually
pip install transformers torch scikit-learn
```

---

## ❌ "run_training.py" fails or hangs

**Problem:** Training doesn't start or gets stuck

**Solutions:**
```bash
# 1. Check if data files exist
# Look in: data/
# - Crop_recommendation.csv
# - Fertilizer Prediction.csv
# - Crop Recommendation using Soil Properties and Weather Prediction.csv

# 2. If missing, you need to add them or get them from your friend

# 3. Try training individual models instead
python training/train_crop_model.py
python training/train_fertilizer_model.py
python training/train_intent_classifier.py

# 4. If BERT training is slow (using CPU), consider GPU
# On Windows with NVIDIA GPU:
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118
```

---

## ❌ Hugging Face authentication failed

**Error:** `huggingface_hub.HfHubHTTPError` or `Invalid token`

**Solutions:**
```bash
# 1. Re-login
huggingface-cli logout
huggingface-cli login

# 2. Get a new token from https://huggingface.co/settings/tokens
# Make sure it has "write" permission

# 3. Paste token when prompted, press Enter

# 4. Verify login worked
huggingface-cli whoami
# Should show your username
```

---

## ❌ "upload_models.py" says models not found

**Error:** `⚠️ Skipping (not found): models/crop_model.pkl`

**Solution:**
```bash
# Make sure you ran training first
python run_training.py
# Or individual scripts:
python training/train_crop_model.py

# Check that models folder exists
# You should see these files in models/:
# - crop_model.pkl
# - fertilizer_model.pkl
# - intent_model/  (folder)
```

---

## ❌ API won't start: "Address already in use"

**Error:** `OSError: [Errno 48] Address already in use` or `[WinError 10048]`

**Solution:**
```bash
# Port 8000 is already in use, use different port
uvicorn api.main:app --reload --host 0.0.0.0 --port 8001

# Or kill the process using port 8000
# On Windows PowerShell:
Get-Process -Id (Get-NetTCPConnection -LocalPort 8000).OwningProcess | Stop-Process -Force

# Then start API again
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ❌ API returns "Module not found" errors

**Error:** When accessing http://localhost:8000/docs

**Solution:**
```bash
# Make sure you're in the correct directory
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"

# Venv is activated
venv\Scripts\activate

# Start from project root (NOT from api/ folder)
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## ❌ Models not downloading from Hugging Face

**Error:** API is slow or "failed to download models"

**Solution:**
```bash
# 1. Check that HF_REPO_ID is correct in api/predictor.py
# Should be: YOUR_USERNAME/agribot-models

# 2. Clear model cache
# On Windows:
rmdir /s %USERPROFILE%\.cache\agribot_models
# On Mac/Linux:
rm -rf ~/.cache/agribot_models

# 3. Make sure models are actually in your HF repo
# Go to: https://huggingface.co/YOUR_USERNAME/agribot-models

# 4. First API call will download ~100MB, takes 30 seconds
# Subsequent calls use cache (instant)

# 5. Check HF token (if repo is private)
# Add to api/predictor.py:
import os
os.environ["HF_TOKEN"] = "your_token_here"
```

---

## ❌ "api/predictor.py" syntax errors

**Error:** `SyntaxError` when starting API

**Solution:**
```bash
# 1. Check file was saved correctly
# Line 9-10 should be:
HF_REPO_ID = "YOUR_USERNAME/agribot-models"
HF_CACHE_DIR = os.path.expanduser("~/.cache/agribot_models")

# 2. Make sure no quotes are broken
# Correct: HF_REPO_ID = "username/repo"
# Wrong: HF_REPO_ID = "username/repo' (mismatched quotes)

# 3. Check indentation (Python is picky!)
# All code should align properly

# 4. Verify with Python
python -m py_compile api/predictor.py
# Should have no output = syntax is OK
```

---

## ❌ Railway deployment keeps failing

**Error:** Deployment fails, red X in Railway dashboard

**Solutions:**
```bash
# 1. Check requirements.txt has all dependencies
# Should include: transformers, torch, fastapi, uvicorn, huggingface_hub
pip freeze > requirements.txt

# 2. Verify Procfile or start command
# Create/check Procfile (no extension):
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT

# 3. Check environment variables in Railway
# Add: HF_REPO_ID = "YOUR_USERNAME/agribot-models"

# 4. Check logs in Railway dashboard
# Click "Deployments" → View latest → "Logs"
# Look for error messages

# 5. Common fixes:
# - Make sure all imports in api/main.py work
# - Test locally first: uvicorn api.main:app --port 8000
# - Commit all changes to GitHub
# - Check Railway has correct GitHub repo connected
```

---

## ❌ Netlify frontend shows blank page

**Error:** Frontend loads but shows nothing

**Solutions:**
```
# 1. Check frontend/index.html exists
# Make sure it's in the frontend/ folder

# 2. Check API_URL is correct
# In frontend/index.html, find:
const API_URL = "http://localhost:8000";
# During Netlify deployment, change to:
const API_URL = "https://YOUR-RAILWAY-DOMAIN";

# 3. Check Railway API is working
# Open: https://YOUR-RAILWAY-DOMAIN/docs
# Should see API documentation

# 4. Check CORS is enabled in api/main.py
# Should have:
app.add_middleware(CORSMiddleware, allow_origins=["*"], ...)

# 5. Check browser console for errors
# Right-click → Inspect → Console tab
# Look for error messages
```

---

## ❌ "ModuleNotFoundError: No module named 'api'"

**Error:** When running scripts in wrong directory

**Solution:**
```bash
# Always run from project ROOT directory:
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"

# Not from subdirectories:
# ❌ cd api/
# ❌ cd training/

# Then run:
python run_training.py
# or
uvicorn api.main:app ...
```

---

## ❌ BERT/Intent model training is VERY SLOW

**Problem:** Takes >30 minutes on CPU

**Solutions:**
```bash
# 1. Use GPU (if you have NVIDIA GPU)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# 2. Skip intent training initially, train other models first
python training/train_crop_model.py
python training/train_fertilizer_model.py
# These are much faster

# 3. Check BERT script settings
# In training/train_intent_classifier.py:
# - Reduce num_train_epochs from 3 to 1
# - Reduce batch_size from 16 to 8
# - Use smaller dataset subset

# 4. Just upload friend's models if you don't need to retrain
# You can skip BERT retraining and use existing models
```

---

## ❌ "ImportError: cannot import name 'weather_api'"

**Error:** In api/main.py

**Solution:**
```bash
# Check that api/weather_api.py exists
# If not, create a simple version:

# Create: api/weather_api.py
def get_weather_advice(location, season):
    return f"Weather advice for {location} in {season}"
```

---

## ✅ All else fails: Nuclear reset

```bash
# Remove everything and start fresh
rmdir /s venv
rmdir /s models
rmdir /s %USERPROFILE%\.cache\agribot_models

# Fresh start
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt

# Train again
python run_training.py

# Upload again
python upload_models.py

# Test API
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

---

## 🆘 Still stuck?

1. **Check the error message carefully** — Most errors tell you exactly what's wrong
2. **Read the traceback** — Look at the last line, it usually says the problem
3. **Check file paths** — Make sure files exist where expected
4. **Check that venv is activated** — Should see `(venv)` at start of terminal line
5. **Restart PowerShell** — Sometimes terminal gets stuck
6. **Look at LOCAL_SETUP_GUIDE.md** — More detailed explanations there

---

## 📞 Quick Debug Checklist

```bash
# 1. Verify Python and venv
python --version  # Should be 3.9+
venv\Scripts\activate
which python  # Should point to venv folder

# 2. Verify dependencies
pip list | grep -E "transformers|fastapi|torch"

# 3. Verify project structure
dir models\  # Should see .pkl and .json files
dir data\    # Should see .csv files
dir api\     # Should see main.py, predictor.py

# 4. Verify HF setup
huggingface-cli whoami  # Should show your username

# 5. Test locally
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
# Open browser: http://localhost:8000/docs

# 6. Test request
curl http://localhost:8000/health
```

