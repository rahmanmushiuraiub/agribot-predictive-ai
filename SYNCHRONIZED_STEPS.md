# 🎯 STEP-BY-STEP SYNCHRONIZED GUIDE - AgriBot Setup

**Start here. Follow ONE step at a time. After each step, wait for success before moving forward.**

---

## ⏹️ STEP 1: Open PowerShell

**DO THIS NOW:**
1. Press `Win + R` (Windows key + R)
2. Type: `powershell`
3. Press Enter

**Expected result:** Black terminal window opens

---

## ⏹️ STEP 2: Navigate to Project

**DO THIS NOW:** Copy and paste this command:

```bash
cd "d:\Nlp project\agribot_v4 (2)\agribot_v4"
```

Press Enter.

**Expected result:** Terminal shows: `PS D:\Nlp project\agribot_v4 (2)\agribot_v4>`

---

## ⏹️ STEP 3: Create Virtual Environment

**DO THIS NOW:** Copy and paste this command:

```bash
python -m venv venv
```

Press Enter.

**Expected result:** Wait 30 seconds. Terminal returns to prompt. A `venv` folder appears in your project.

**Verify:** Right-click project folder → "Open in Files" → You should see a `venv` folder now.

---

## ⏹️ STEP 4: Activate Virtual Environment

**DO THIS NOW:** Copy and paste this command:

```bash
venv\Scripts\activate
```

Press Enter.

**Expected result:** Terminal line changes to: `(venv) PS D:\Nlp project\agribot_v4 (2)\agribot_v4>`

**Important:** Notice `(venv)` at the beginning. This means venv is active.

---

## ⏹️ STEP 5: Install Dependencies

**DO THIS NOW:** Copy and paste this command:

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

Press Enter.

**Expected result:** 
- Installation starts
- Wait 3-5 minutes
- See green checkmarks (✓)
- Terminal returns to prompt

**Verify:** End of output should say "Successfully installed..." or "already satisfied"

---

## ⏹️ STEP 6: Train Models (Most Important!)

**DO THIS NOW:** Copy and paste this command:

```bash
python run_training.py
```

Press Enter.

**Expected result:**
```
Starting crop model training...
[████████████████] 100%
Crop model trained and saved!

Starting fertilizer model training...
[████████████████] 100%
Fertilizer model trained and saved!

Starting intent classifier training...
[████████████████] 100%
Intent classifier trained and saved!

All models trained successfully!
```

**⏱️ This takes 15-20 minutes. Go grab coffee. ☕**

**After it finishes:**
1. Right-click project folder → "Open in Files"
2. Go to `models/` folder
3. You should see NEW files:
   - `crop_model.pkl`
   - `fertilizer_model.pkl`
   - `intent_model/` (folder)

---

## ⏹️ STEP 7: Create Hugging Face Account

**DO THIS NOW (use your browser, not terminal):**

1. Go to: https://huggingface.co/
2. Click blue "Sign Up" button
3. Fill in: Email, Username, Password
4. Click "Create Account"
5. **Check your email** - Click verification link
6. Done! You're logged in

**Expected result:** You see Hugging Face dashboard

---

## ⏹️ STEP 8: Create Hugging Face API Token

**DO THIS NOW (in browser):**

1. Go to: https://huggingface.co/settings/tokens
2. Click blue "New token" button
3. Fill in:
   - Name: `agribot-upload` (just a name)
   - Role: Select `write` from dropdown
4. Click "Create token"
5. **Copy the token** (it's a long string)
6. **Paste it somewhere safe** (Notepad, etc.) - You need it next

**Expected result:** You have a token that looks like: `hf_abc123def456...`

---

## ⏹️ STEP 9: Create Hugging Face Model Repository

**DO THIS NOW (in browser):**

1. Go to: https://huggingface.co/new
2. Fill in:
   - **Repository name:** `agribot-models` (EXACTLY this)
   - **Repository type:** Select "Model"
   - **Visibility:** Select "Public"
3. Click "Create repository"
4. Done!

**Expected result:** You see a page with your repo URL. Copy it. It looks like:
```
https://huggingface.co/YOUR_USERNAME/agribot-models
```

**Save this URL - you need it soon!**

---

## ⏹️ STEP 10: Login to Hugging Face (Terminal)

**DO THIS NOW:** Back in PowerShell terminal (should still have `(venv)` prefix)

Copy and paste:

```bash
huggingface-cli login
```

Press Enter.

**Expected result:** Terminal says: `Token:`

**DO THIS NOW:**
1. **Paste your API token** (from Step 8)
2. Press Enter
3. Terminal says: `Token is valid`

**Great! You're logged in.**

---

## ⏹️ STEP 11: Upload Models to Hugging Face

**DO THIS NOW:** In PowerShell terminal

Copy and paste:

```bash
python upload_models.py
```

Press Enter.

**Expected result:**
```
🚀 Starting upload to: YOUR_USERNAME/agribot-models
============================================================

📤 Uploading model files...
  • Uploading crop_model.pkl... ✅
  • Uploading crop_label_encoder.pkl... ✅
  • Uploading crop_scaler.pkl... ✅
  • Uploading fertilizer_model.pkl... ✅
  • Uploading fertilizer_encoders.pkl... ✅
  • Uploading fertilizer_scaler.pkl... ✅
  • Uploading fertilizer_meta.json... ✅
  • Uploading intent_model/... ✅

✅ Upload complete!
   • Successfully uploaded: 8
   📍 Repository: https://huggingface.co/YOUR_USERNAME/agribot-models
```

**⏱️ This takes 2-5 minutes (uploads ~100MB)**

---

## ⏹️ STEP 12: Verify Models Uploaded

**DO THIS NOW (in browser):**

1. Go to: `https://huggingface.co/YOUR_USERNAME/agribot-models`
2. You should see files listed:
   - crop_model.pkl
   - fertilizer_model.pkl
   - intent_model folder
   - etc.

**Great! Models are in the cloud now.**

---

## ⏹️ STEP 13: Update API Configuration

**DO THIS NOW (in VS Code):**

1. Open file: `api/predictor.py`
2. Find line 9-10 (near top):
   ```python
   HF_REPO_ID = "MushiurRahmanAi/AgribotMushiur"
   HF_CACHE_DIR = os.path.expanduser("~/.cache/agribot_models")
   ```

3. **Change line 9 to YOUR username:**
   ```python
   HF_REPO_ID = "YOUR_USERNAME/agribot-models"
   ```

   Example: If your HF username is `john_doe`:
   ```python
   HF_REPO_ID = "john_doe/agribot-models"
   ```

4. Press `Ctrl + S` to save

**Expected result:** File is saved (no orange dot on tab)

---

## ⏹️ STEP 14: Test API Locally

**DO THIS NOW:** Back in PowerShell terminal

Make sure `(venv)` is showing. If not, run:
```bash
venv\Scripts\activate
```

Then copy and paste:

```bash
uvicorn api.main:app --reload --host 0.0.0.0 --port 8000
```

Press Enter.

**Expected result:**
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete
```

**Keep this terminal open!**

---

## ⏹️ STEP 15: Test API in Browser

**DO THIS NOW (open browser):**

1. Open new tab
2. Go to: `http://localhost:8000/docs`
3. You should see beautiful API documentation

**Expected result:** Blue Swagger UI page with endpoints listed

---

## ⏹️ STEP 16: Test Crop Prediction Endpoint

**DO THIS NOW (in browser, on the /docs page):**

1. Find "POST /predict/crop" (scroll down)
2. Click on it (it expands)
3. Click "Try it out" button
4. You see a JSON box with example values
5. Scroll to the JSON editor and paste:

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

6. Click blue "Execute" button

**Expected result:**
```json
{
  "top_3_crops": [
    "Rice",
    "Wheat",
    "Maize"
  ]
}
```

**✅ YES! API is working!**

---

## ⏹️ STEP 17: Test Chat Endpoint

**Still on the /docs page:**

1. Find "POST /chat" endpoint
2. Click on it
3. Click "Try it out"
4. Paste:

```json
{
  "message": "My rice leaves are turning yellow"
}
```

5. Click "Execute"

**Expected result:**
```json
{
  "intent": "disease_identification",
  "confidence": 0.95,
  "response": "This is likely leaf blast or blast disease..."
}
```

**✅ Chat working too!**

---

## ⏹️ STEP 18: Test Frontend Locally

**DO THIS NOW (in browser):**

1. Open new tab
2. Go to: `file:///d:/Nlp%20project/agribot_v4%20(2)/agribot_v4/frontend/index.html`
3. You see the chatbot interface
4. Try sending a message: "What crop should I grow?"
5. You should get an answer

**✅ Frontend working!**

---

## ⏹️ STEP 19: Create Railway Account

**DO THIS NOW (in browser):**

1. Go to: https://railway.app/
2. Click "Login" (top right) → Choose "GitHub"
3. Complete GitHub login
4. Done! You're in Railway

---

## ⏹️ STEP 20: Deploy on Railway

**DO THIS NOW (in Railway dashboard):**

1. Click "Create" button
2. Click "New Project"
3. Click "Deploy from GitHub repo"
4. Find and select your agribot repo: `agribot_v4`
5. Click "Deploy"

**⏱️ Wait 2-3 minutes for deployment...**

**Expected result:** Green checkmark, status = "Deployed"

---

## ⏹️ STEP 21: Add Environment Variables to Railway

**DO THIS NOW:**

1. In Railway dashboard, click your project
2. Click "Variables" tab
3. Add new variable:
   - Key: `HF_REPO_ID`
   - Value: `YOUR_USERNAME/agribot-models` (same as Step 13)
4. Click "Add"
5. **Redeploy** - Click "Deployments" → Choose latest → Menu → "Redeploy"

**⏱️ Wait 1-2 minutes...**

---

## ⏹️ STEP 22: Get Your Railway Domain

**DO THIS NOW:**

1. In Railway, go to "Settings" tab
2. Find "Domains" section
3. Copy the domain (looks like): `https://agribot-prod-xxxx.up.railway.app`
4. **Save this URL** - You need it next

---

## ⏹️ STEP 23: Test Railway Backend

**DO THIS NOW (in terminal/PowerShell):**

Open NEW PowerShell window (leave old one running). Paste:

```bash
curl https://YOUR-RAILWAY-DOMAIN/health
```

Replace `YOUR-RAILWAY-DOMAIN` with your actual domain from Step 22.

Press Enter.

**Expected result:**
```json
{"status":"ok"}
```

**✅ Railway backend is working!**

---

## ⏹️ STEP 24: Update Frontend with Railway URL

**DO THIS NOW (in VS Code):**

1. Open: `frontend/index.html`
2. Find line with: `const API_URL = "http://localhost:8000";`
3. Change it to:
   ```javascript
   const API_URL = "https://YOUR-RAILWAY-DOMAIN";
   ```

   Example:
   ```javascript
   const API_URL = "https://agribot-prod-xxxx.up.railway.app";
   ```

4. Press `Ctrl + S` to save

---

## ⏹️ STEP 25: Deploy Frontend on Netlify

**DO THIS NOW:**

1. Go to: https://netlify.com/
2. Login with GitHub
3. Click "New site from Git"
4. Select your agribot repo
5. Configure build:
   - Build command: (leave blank)
   - Publish directory: `frontend`
6. Click "Deploy site"

**⏱️ Wait 1-2 minutes...**

**Expected result:** Your site is live! Netlify gives you a URL like: `https://agribot-xxxx.netlify.app`

---

## ⏹️ FINAL STEP 26: Test End-to-End

**DO THIS NOW:**

1. Open your Netlify URL in browser: `https://agribot-xxxx.netlify.app`
2. Type a message: `"My wheat is wilting"`
3. Click "Send"

**Expected result:**
- Frontend sends message → Railway backend → Downloads models from HF Hub → Returns answer → Shows in frontend

**✅ EVERYTHING WORKS! 🎉**

---

## 📊 What You've Done

| Step | Task | Where |
|------|------|-------|
| 1-6 | Local setup & training | Your laptop ✓ |
| 7-12 | Upload models | Hugging Face Hub ✓ |
| 13 | Update API config | VS Code ✓ |
| 14-18 | Test locally | Localhost:8000 ✓ |
| 19-23 | Deploy backend | Railway ✓ |
| 24-26 | Deploy frontend | Netlify ✓ |

---

## 🎯 Result

```
Your Frontend (Netlify)
        ↓
    Railway Backend
        ↓
Hugging Face Hub (Models)
```

**All connected and working! 🚀**

---

## 📝 Save These URLs

Keep them somewhere safe (Notepad):

- **HF Repo:** https://huggingface.co/YOUR_USERNAME/agribot-models
- **Railway Backend:** https://YOUR-RAILWAY-DOMAIN
- **Netlify Frontend:** https://YOUR-NETLIFY-DOMAIN.netlify.app

---

## 🆘 Something didn't work?

- Check **TROUBLESHOOTING.md** for solutions
- Each step has "Expected result" - if you don't see it, something's wrong
- Re-read the step carefully and try again

---

**That's it! You're done. Your AgriBot is live! 🌱**

