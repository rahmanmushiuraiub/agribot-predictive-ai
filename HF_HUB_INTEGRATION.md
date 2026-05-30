# Hugging Face Hub Integration Guide

## Overview

Your AgriBot backend now fetches models from Hugging Face Hub (`Toyeb/agribot-models`) instead of local storage. This guide covers setup, configuration, and deployment.

---

## ✅ Changes Made to Backend

### Modified File: `api/predictor.py`

**Key Changes:**

1. Added import: `from huggingface_hub import hf_hub_download`
2. Configured Hub repository:
   ```python
   HF_REPO_ID = "Toyeb/agribot-models"
   HF_CACHE_DIR = os.path.expanduser("~/.cache/agribot_models")
   ```
3. Updated all `_load_*()` functions to:
   - Download models from HF Hub on-demand (first request downloads, subsequent use cache)
   - Cache models locally for faster subsequent requests
   - Handle missing models gracefully with try/except

### What's Already in requirements.txt

✓ `huggingface_hub` - Already included!

---

## 📦 How to Upload Models to Hugging Face Hub

### Step 1: Install Dependencies

```bash
pip install huggingface-hub huggingface-cli
```

### Step 2: Login to Hugging Face

```bash
huggingface-cli login
# Paste your HF token when prompted
```

### Step 3: Create Hugging Face Repository

Go to https://huggingface.co/new and create a new model repo named `agribot-models`.

### Step 4: Upload Your Model Files

**Option A: Using Python Script**

```python
from huggingface_hub import HfApi, HfFolder

api = HfApi()
repo_id = "Toyeb/agribot-models"

# Upload model files
api.upload_file(
    path_or_fileobj="models/crop_model.pkl",
    path_in_repo="crop_model.pkl",
    repo_id=repo_id,
)

api.upload_file(
    path_or_fileobj="models/crop_label_encoder.pkl",
    path_in_repo="crop_label_encoder.pkl",
    repo_id=repo_id,
)

api.upload_file(
    path_or_fileobj="models/crop_scaler.pkl",
    path_in_repo="crop_scaler.pkl",
    repo_id=repo_id,
)

# ... repeat for all .pkl files ...

api.upload_file(
    path_or_fileobj="models/crop_meta.json",
    path_in_repo="crop_meta.json",
    repo_id=repo_id,
)
# ... repeat for all .json files ...

# Upload intent model as folder
api.upload_folder(
    folder_path="models/intent_model",
    repo_id=repo_id,
    path_in_repo="intent_model",
)
```

**Option B: Using Git (Faster)**

```bash
cd ~/tmp
git clone https://huggingface.co/Toyeb/agribot-models
cd agribot-models
cp -r ../agribot_v4/models/* .
git add .
git commit -m "Add trained models"
git push
```

**Option C: Web UI**

- Go to https://huggingface.co/Toyeb/agribot-models/tree/main
- Click "Add file" → "Upload files" and select files from your `models/` directory

---

## 🚀 Deployment Configuration

### Railway Backend (`.env` or deployment settings)

```
HF_REPO_ID=Toyeb/agribot-models
HF_CACHE_DIR=/tmp/agribot_cache  # Railway has /tmp, /workspace, etc.
# Optional: if models are private
HF_TOKEN=your_hf_token_here
```

### For Private Models (if needed)

In `api/predictor.py`, models can accept a token:

```python
# Example for private repos:
_crop_model = joblib.load(
    hf_hub_download(
        repo_id=HF_REPO_ID,
        filename="crop_model.pkl",
        cache_dir=HF_CACHE_DIR,
        token=os.getenv("HF_TOKEN")  # Add this line
    )
)
```

---

## 🔄 How It Works (Model Loading Flow)

### First Time (Cold Start)

1. API receives prediction request
2. `_load_crop()` is called
3. `hf_hub_download()` downloads from HF Hub → caches locally
4. Model predictions proceed

### Subsequent Times (Warm Cache)

1. API checks if model already cached
2. Returns from local cache (instant)
3. No HF Hub download needed

**Cache Location:**

- Local development: `~/.cache/agribot_models/`
- Railway: `/tmp/agribot_cache/` (or configured path)

---

## ✨ Special Handling: Intent Model (Transformer)

The intent model is handled differently because it's a **HuggingFace-native model**:

```python
# Directly uses from_pretrained() with HF model card
_intent_model = DistilBertForSequenceClassification.from_pretrained(
    f"{HF_REPO_ID}/intent_model",
    cache_dir=HF_CACHE_DIR
)
```

This requires your intent model to be in the HF Hub repo as a valid model directory with:

- `config.json`
- `pytorch_model.bin` (or `model.safetensors`)
- `tokenizer.json`
- `vocab.txt`

---

## 🛠️ Troubleshooting

### Issue: "404 Model not found"

**Solution:** Ensure files exist in your HF Hub repo at `Toyeb/agribot-models`

```bash
huggingface-cli list-repo-files Toyeb/agribot-models
```

### Issue: "Permission denied" when downloading

**Solution:** If models are private, add token:

```python
token=os.getenv("HF_TOKEN")
```

### Issue: Cache grows too large

**Solution:** Periodically clean HF cache:

```bash
python -c "from huggingface_hub import scan_cache_dir; cache_info = scan_cache_dir(); print(cache_info); cache_info.delete_revisions(*list(cache_info.revisions)[:5])"
```

### Issue: Timeout on Railway

**Solution:** Increase timeout in FastAPI startup:

```python
# in api/main.py
import httpx
httpx.Client(timeout=60.0)
```

---

## 📋 Checklist

- [ ] Upload all `.pkl` files to HF Hub repo
- [ ] Upload all `.json` files to HF Hub repo
- [ ] Upload `intent_model/` folder with required files
- [ ] Set `HF_REPO_ID = "Toyeb/agribot-models"` in `predictor.py` ✅ (Done)
- [ ] Test locally: `python -c "from api.predictor import predict_crop; print(predict_crop(40, 60, 40, 20, 80, 6.5, 200))"`
- [ ] Deploy to Railway
- [ ] Test production API endpoints

---

## 🔗 Useful Links

- HF Hub Python API: https://huggingface.co/docs/hub/security-tokens
- Your Model Repo: https://huggingface.co/Toyeb/agribot-models
- Cache Management: https://huggingface.co/docs/hub/security-tokens#cache-management
