"""
upload_models.py — Upload trained models to Hugging Face Hub
Run this after training your models locally
"""

import os
from huggingface_hub import HfApi

def main():
    # Initialize API
    api = HfApi()
    
    # Get username
    try:
        user_info = api.whoami()
        username = user_info['name']
    except Exception as e:
        print(f"❌ Error: {e}")
        print("Make sure you're logged in: huggingface-cli login")
        return
    
    repo_id = os.getenv("HF_REPO_ID", f"{username}/agribot-models")
    print(f"\n🚀 Starting upload to: {repo_id}")
    print("=" * 60)

    # Ensure the target repository exists on the Hub
    try:
        api.create_repo(repo_id=repo_id, private=False, exist_ok=True)
    except Exception as e:
        print(f"⚠️  Repo creation/check failed: {e}")
        print("    If the repo already exists, make sure your token has write access.")
        print("    If it does not exist, create it on Hugging Face or set HF_REPO_ID to an existing repo.")
        return
    
    # Model files to upload
    model_files = [
        ("models/crop_model.pkl", "crop_model.pkl"),
        ("models/crop_label_encoder.pkl", "crop_label_encoder.pkl"),
        ("models/crop_scaler.pkl", "crop_scaler.pkl"),
        ("models/crop_meta.json", "crop_meta.json"),
        ("models/fertilizer_model.pkl", "fertilizer_model.pkl"),
        ("models/fertilizer_encoders.pkl", "fertilizer_encoders.pkl"),
        ("models/fertilizer_scaler.pkl", "fertilizer_scaler.pkl"),
        ("models/fertilizer_meta.json", "fertilizer_meta.json"),
        ("models/crop_stats.json", "crop_stats.json"),
        ("models/yield_meta.json", "yield_meta.json"),
        ("models/state_profiles.json", "state_profiles.json"),
    ]
    
    # Upload individual files
    uploaded_count = 0
    failed_count = 0
    
    print("\n📤 Uploading model files...")
    for local_path, remote_name in model_files:
        if not os.path.exists(local_path):
            print(f"⚠️  Skipping (not found): {local_path}")
            continue
        
        try:
            print(f"  • Uploading {remote_name}...", end=" ", flush=True)
            api.upload_file(
                path_or_fileobj=local_path,
                path_in_repo=remote_name,
                repo_id=repo_id,
                commit_message=f"Upload {remote_name}"
            )
            print("✅")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ ({e})")
            failed_count += 1
    
    # Upload intent model folder
    intent_model_path = "models/intent_model"
    if os.path.exists(intent_model_path):
        try:
            print(f"  • Uploading intent_model/...", end=" ", flush=True)
            api.upload_folder(
                folder_path=intent_model_path,
                repo_id=repo_id,
                path_in_repo="intent_model",
                commit_message="Upload BERT intent classifier"
            )
            print("✅")
            uploaded_count += 1
        except Exception as e:
            print(f"❌ ({e})")
            failed_count += 1
    else:
        print(f"⚠️  Skipping (not found): {intent_model_path}")
    
    # Summary
    print("\n" + "=" * 60)
    print(f"✅ Upload complete!")
    print(f"   • Successfully uploaded: {uploaded_count}")
    if failed_count > 0:
        print(f"   • Failed: {failed_count}")
    print(f"\n📍 Repository: https://huggingface.co/{repo_id}")
    print(f"   Use this in api/predictor.py:")
    print(f"   HF_REPO_ID = \"{repo_id}\"")

if __name__ == "__main__":
    main()
