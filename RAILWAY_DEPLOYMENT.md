# Railway Deployment Configuration for Hugging Face Hub

## Environment Variables for Railway

When deploying on Railway, add these environment variables in your Railway project settings:

### Required Variables

```
HF_REPO_ID=Toyeb/agribot-models
```

### Optional Variables (for private models or customization)

```
HF_CACHE_DIR=/tmp/agribot_models
HF_TOKEN=your_hf_api_token_here  # Only if models are private
```

---

## Step-by-Step Railway Deployment

### 1. Connect Your Repository

- Go to https://railway.app/
- Create a new project
- Connect your GitHub repo (agribot_v4)
- Railway auto-detects Python project

### 2. Add Environment Variables

Click "Variables" in Railway dashboard and add:

| Key            | Value                           | Required    |
| -------------- | ------------------------------- | ----------- |
| `HF_REPO_ID`   | `Toyeb/agribot-models`          | ✅ Yes      |
| `HF_CACHE_DIR` | `/tmp/agribot_models`           | ⭕ Optional |
| `HF_TOKEN`     | (leave blank for public models) | ⭕ Optional |

### 3. Configure Start Command

In Railway build/start settings:

```bash
# Build command (optional):
pip install -r requirements.txt

# Start command:
uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

Or add `Procfile` to root:

```
web: uvicorn api.main:app --host 0.0.0.0 --port $PORT
```

### 4. Check Logs

After deployment, check logs for:

```
INFO:     Uvicorn running on http://0.0.0.0:PORT
```

Make a test request:

```bash
curl https://your-railway-domain.up.railway.app/health
```

---

## Frontend Integration (Netlify)

Your Netlify-hosted frontend should call:

```javascript
const API_BASE = "https://your-railway-domain.up.railway.app";

// Example: Crop prediction
fetch(`${API_BASE}/predict/crop`, {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify({
    N: 90,
    P: 42,
    K: 43,
    temperature: 25,
    humidity: 80,
    ph: 6.5,
    rainfall: 200,
  }),
})
  .then((r) => r.json())
  .then((data) => console.log(data));
```

---

## Cache Management on Railway

Railroad provides ephemeral storage (deleted on redeploy). To manage cache:

### Option 1: Accept Fresh Downloads (Recommended)

- No setup needed
- First request downloads models (~50-500MB total)
- Subsequent requests use cache for that session
- Cache cleared on redeploy (fresh start)

### Option 2: Use Railway Database (Persistent Cache)

If you want persistent cache across redeploys:

```python
# In api/predictor.py
import os

# Use Railway's PostgreSQL for caching (advanced)
# OR use Railway's Volumes (persistent storage)

HF_CACHE_DIR = os.getenv("HF_CACHE_DIR", "/railway/models")
```

Then attach a Volume in Railway:

- Mount path: `/railway/models`
- Size: 10GB (adjust as needed)

---

## Performance Tips

1. **First Cold Start**: ~2-3 minutes (downloading models)
2. **Subsequent Requests**: <1 second (cached)
3. **Keep Models Public**: Faster, no token needed
4. **Use `hf_hub_download`**: Already handles caching optimally

---

## Troubleshooting Railway Deployment

### Issue: `HfHubHTTPError: 404 Client Error`

**Cause**: Model repo doesn't exist or file not found  
**Solution**:

```bash
# Check repo contents:
huggingface-cli list-repo-files Toyeb/agribot-models
```

### Issue: `Timeout` on first request

**Cause**: Large models downloading  
**Solution**: Increase Railway timeout or use persistent volume

### Issue: Memory exceeded

**Cause**: Models too large for Railway tier  
**Solution**:

- Upgrade Railway tier, or
- Quantize models (reduce size 50-80%), or
- Use ONNX runtime (lighter than PyTorch)

---

## Production Checklist

- [ ] Upload all models to `Toyeb/agribot-models` repo
- [ ] Test locally with `python upload_models_to_hf.py`
- [ ] Set `HF_REPO_ID` in Railway variables
- [ ] Deploy to Railway
- [ ] Test cold start (first request)
- [ ] Test warm cache (second request)
- [ ] Test from Netlify frontend
- [ ] Set up custom domain (optional)
- [ ] Monitor Railway logs for errors

---

## Cost Estimate

| Service      | Cost         | Notes                   |
| ------------ | ------------ | ----------------------- |
| Railway      | $5/month     | Starter plan sufficient |
| Hugging Face | Free         | 12GB storage free       |
| Netlify      | Free         | Generous free tier      |
| **Total**    | **$5/month** | No per-request charges  |
