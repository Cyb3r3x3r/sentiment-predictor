import argparse
import json
import os
import random

import numpy as np
import torch
from torch.nn import CrossEntropyLoss
from torch.utils.data import DataLoader
from transformers import AutoTokenizer,AutoModelForSequenceClassification,AdamW,get_scheduler

from datasets import load_dataset,Dataset

# Setting random seeds
def set_all_seeds(seed=42):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)

LABEL_MAP = {"negative": 0, "positive": 1}
MODEL_NAME = "distilbert-base-uncased"
MODEL_DIR = "../model"


# function to load dataset from jsonl file
def load_dataset_jsonl(path):
    examples = []
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            record = json.loads(line)
            if record["label"] not in LABEL_MAP:
                continue
            examples.append({
                "text": record["text"],
                "label": LABEL_MAP[record["label"]]
            })
    return Dataset.from_list(examples)


# preparing the samples to pass them into model
def collate_fn(batch, tokenizer):
    texts = [item["text"] for item in batch]
    labels = [item["label"] for item in batch]
    encodings = tokenizer(texts, padding=True, truncation=True, return_tensors="pt")
    encodings["labels"] = torch.tensor(labels)
    return encodings

def train(args):
    set_all_seeds(42)

    # Load data
    dataset = load_dataset_jsonl(args.data)
    dataset = dataset.shuffle(seed=42)
    split = dataset.train_test_split(test_size=0.2)
    train_ds = split["train"]
    val_ds = split["test"]

    tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_NAME, num_labels=2)
    model.config.id2label = {0: "negative", 1: "positive"}
    model.config.label2id = {"negative": 0, "positive": 1}


    train_loader = DataLoader(
        train_ds, batch_size=8, shuffle=True,
        collate_fn=lambda x: collate_fn(x, tokenizer)
    )
    val_loader = DataLoader(
        val_ds, batch_size=8,
        collate_fn=lambda x: collate_fn(x, tokenizer)
    )

    # Optimizer and scheduler
    optimizer = AdamW(model.parameters(), lr=args.lr)
    num_training_steps = args.epochs * len(train_loader)
    scheduler = get_scheduler("linear", optimizer=optimizer, num_warmup_steps=0, num_training_steps=num_training_steps)

    model.train()
    for epoch in range(args.epochs):
        total_loss = 0
        for batch in train_loader:
            optimizer.zero_grad()
            outputs = model(**batch)
            loss = outputs.loss
            total_loss += loss.item()

            loss.backward()
            torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)  # Gradient clipping
            optimizer.step()
            scheduler.step()

        print(f"Epoch {epoch+1}/{args.epochs} - Loss: {total_loss:.4f}")

    # Save model and tokenizer
    print("✅ Saving fine-tuned model to ./model/")
    model.save_pretrained(MODEL_DIR, safe_serialization=False)
    tokenizer.save_pretrained(MODEL_DIR)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("-data", type=str, required=True, help="Path to training data (JSONL)")
    parser.add_argument("-epochs", type=int, default=3, help="Number of epochs")
    parser.add_argument("-lr", type=float, default=3e-5, help="Learning rate")
    args = parser.parse_args()

    train(args)