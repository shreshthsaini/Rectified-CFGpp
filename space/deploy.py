"""Publish this folder as a Hugging Face Space.

Needs a logged-in account (`hf auth login`) on a plan that can host Gradio
Spaces, and access to the gated backbone weights. Requests ZeroGPU and stores
your token as the Space's HF_TOKEN secret so the backbone can be downloaded.

    python space/deploy.py [namespace/space-name]
"""

import os
import sys

from huggingface_hub import HfApi

DEFAULT = "shreshthsaini/Rectified-CFGpp"
HERE = os.path.dirname(os.path.abspath(__file__))

api = HfApi()
rid = sys.argv[1] if len(sys.argv) > 1 else DEFAULT
api.create_repo(rid, repo_type="space", space_sdk="gradio", exist_ok=True)
api.upload_folder(repo_id=rid, repo_type="space", folder_path=HERE, ignore_patterns=["deploy.py", "__pycache__/*"], commit_message="Deploy demo")
if api.token:
    api.add_space_secret(rid, "HF_TOKEN", api.token)
try:
    api.request_space_hardware(rid, "zero-a10g")
    print("requested ZeroGPU")
except Exception as e:  # not every plan can request it; the Space still builds on CPU
    print("hardware request failed:", e)
print(f"https://huggingface.co/spaces/{rid}")
