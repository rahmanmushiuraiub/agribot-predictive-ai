#!/usr/bin/env python
"""
upload_models_to_hf.py
Upload all trained models from local /models directory to Hugging Face Hub
Run this once to push all models to your HF Hub repo.
"""

import os
import json
from pathlib import Path
from huggingface_hub import HfApi
from huggingface_hub import get_token

# Configuration
HF_REPO_ID = "MushiurRahmanAi/agribot-models"
LOCAL_MODELS_DIR = os.path.join(os.path.dirname(__file__), "models")

def upload_models():
    """Upload all models to Hugging Face Hub"""
    
    print(f"📤 Starting model upload to {HF_REPO_ID}...")
    print(f"📁 Local model directory: {LOCAL_MODELS_DIR}\n")
    
    api = HfApi()
    
    # List of files to upload (adjust based on your actual files)
    files_to_upload = [
        # Crop prediction models
        "crop_model.pkl",
        "crop_label_encoder.pkl",
        "crop_scaler.pkl",
        "crop_meta.json",
        "crop_stats.json",
        
        # Fertilizer prediction models
        "fertilizer_model.pkl",
        "fertilizer_encoders.pkl",
        "fertilizer_scaler.pkl",
        "fertilizer_meta.json",
        
        # Yield prediction models
        "yield_model.pkl",
        "yield_scaler.pkl",
        "yield_meta.json",
        
        # Other metadata
        "state_profiles.json",
        "xgb_crop_meta.json",
        "crop_yield_stats.json",
        "comparison_crop_rf_vs_xgb.json",
    ]
    
    print("📋 Uploading individual model files...\n")
    uploaded_count = 0
    failed_count = 0
    
    for filename in files_to_upload:
        file_path = os.path.join(LOCAL_MODELS_DIR, filename)
        
        if not os.path.exists(file_path):
            print(f"⚠️  SKIP: {filename} (file not found)")
            continue
        
        try:
            print(f"⏳ Uploading: {filename}...", end=" ")
            api.upload_file(
                path_or_fileobj=file_path,
                path_in_repo=filename,
                repo_id=HF_REPO_ID,
                repo_type="model",
                commit_message=f"Add {filename}"
            )
            print("✅")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed_count += 1
    
    # Upload intent model folder
    print("\n📁 Uploading intent model folder...", end=" ")
    intent_dir = os.path.join(LOCAL_MODELS_DIR, "intent_model")
    if os.path.exists(intent_dir):
        try:
            api.upload_folder(
                folder_path=intent_dir,
                repo_id=HF_REPO_ID,
                repo_type="model",
                path_in_repo="intent_model",
                commit_message="Add intent model"
            )
            print("✅")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            failed_count += 1
    else:
        print("⚠️  SKIP (folder not found)")
    
    # Summary
    print(f"\n{'='*50}")
    print(f"Upload Complete!")
    print(f"✅ Uploaded: {uploaded_count}")
    print(f"❌ Failed: {failed_count}")
    print(f"{'='*50}")
    
    if failed_count == 0:
        print(f"\n🎉 All models uploaded to {HF_REPO_ID}")
        print(f"View at: https://huggingface.co/{HF_REPO_ID}")
    else:
        print(f"\n⚠️  Some uploads failed. Check errors above.")

if __name__ == "__main__":
    import sys
    
    # Check if user is logged in
    try:
        token = get_token()
        if not token:
            print("❌ Not logged in to Hugging Face")
            print("Run: huggingface-cli login")
            sys.exit(1)
    except Exception as e:
        print(f"❌ Error checking login status: {e}")
        sys.exit(1)
    
    # Confirm before uploading
    print(f"This will upload all models to: {HF_REPO_ID}")
    confirm = input("Continue? (y/n): ").strip().lower()
    
    if confirm == 'y':
        upload_models()
    else:
        print("Cancelled.")
