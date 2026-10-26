import os
from pathlib import Path

try:
    from dotenv import load_dotenv; load_dotenv()
except ImportError:
    pass

REPO_ROOT = Path(__file__).resolve().parents[2]

def runtime() -> str:
    if Path("/kaggle").exists(): return "kaggle"
    if Path("/var/colab").exists(): return "colab"
    return "local"

def workdir() -> Path:
    return {"kaggle": Path("/kaggle/working"), "colab": Path("/content")}.get(runtime(), REPO_ROOT / ".cache")

def get_secret(name: str):
    if os.environ.get(name):
        return os.environ[name]
    try:
        if runtime() == "kaggle":
            from kaggle_secrets import UserSecretsClient
            return UserSecretsClient().get_secret(name)
        if runtime() == "colab":
            from google.colab import userdata
            return userdata.get(name)
    except Exception:
        pass
    return None