from transformers import pipeline,AutoModelForSequenceClassification,AutoTokenizer
import os


MODEL_NAME = "distilbert-base-uncased-finetuned-sst-2-english"
MODEL_DIR = "../model"

def load_model():
    if os.path.exists(MODEL_DIR):
        print("Loading the fine tuned model from ./model....")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_DIR)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_DIR)
    else:
        print("Loading default model from HuggingFace Hub...")
        model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME)
        tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)

    return pipeline("sentiment-analysis",model=model,tokenizer=tokenizer)