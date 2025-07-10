from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer
import os

MODEL_NAME = "mrm8488/deberta-v3-small-finetuned-sst2"
MODEL_DIR = "./model"  # 👈 Changed from "../model" to "./model"

def load_model():
    required_files = ["config.json", "pytorch_model.bin", "tokenizer_config.json"]
    if (
        os.path.isdir(MODEL_DIR)
        and all(os.path.exists(os.path.join(MODEL_DIR, f)) for f in required_files)
    ):
        print("✅ Loading the fine-tuned model from ./model...")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    else:
        print("ℹ️ Fine-tuned model not found. Loading default model from HuggingFace Hub...")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    return pipeline("sentiment-analysis", model=model, tokenizer=tokenizer)
