import torch
from huggingface_hub import snapshot_download
from transformers import AutoModelForCausalLM, AutoTokenizer
from geo.env import workdir, get_secret

def load_model(model_id="Qwen/Qwen3-4B"):
    path = workdir() / model_id.split("/")[-1]
    snapshot_download(model_id, local_dir=path, token=get_secret("HF_TOKEN"))
    bf16 = torch.cuda.is_available() and torch.cuda.get_device_capability(0)[0] >= 8
    tok = AutoTokenizer.from_pretrained(path)
    model = AutoModelForCausalLM.from_pretrained(
        path, dtype=torch.bfloat16 if bf16 else torch.float16, device_map="auto")
    return tok, model