# 🧠 Sentiment Analysis Microservice

An end-to-end containerized microservice for **binary sentiment classification** using Hugging Face Transformers. Includes:

- Python **FastAPI backend** for inference
- Fine-tuning script with CLI
- Minimal **React frontend** (Vite) for user input
- **Docker Compose** setup for full local development

---

## 🚀 Setup & Run Instructions

### 🔧 Prerequisites

- Docker & Docker Compose installed
- (Optional) Python 3.10+ and Node.js for local development without Docker

---

### 🐳 Run Everything via Docker

From the project root:

```bash
docker-compose up --build
```

- Backend (FastAPI) → http://localhost:8080
- Frontend (React) → http://localhost:3000

### 🧪 Test the API

Swagger UI available at:
```
http://localhost:8080/docs
```

### 🛠 Design Decisions

* FastAPI backend with Hugging Face pipeline() abstraction for simplicity and speed
* Automatically loads latest fine-tuned model from ```./model``` on container start
* Fine-tune script ```(finetune.py)``` saves weights directly to ```./model/```
* React frontend uses fetch to call backend /predict API
* Fully containerized with Docker Compose, using CPU-only compatible base images
* Supports model formats with ```pytorch_model.bin```   

### 🧪 Fine-Tuning

Use the provided CLI:
```bash
python finetune.py -data data.jsonl -epochs 3 -lr 3e-5
```

Each line of data.jsonl should look like:
```json
{"text": "Amazing service!", "label": "positive"}
```
Fine-tuned weights are saved to ./model/ and loaded by the backend automatically.


### ⏱️ CPU Fine-Tune Times

| Hardware     | Dataset Size | Epochs | Time        |
| ------------ | ------------ | ------ | ----------- |
| CPU (8-core) | 50 samples   | 10      | \~30–40 sec |

⏱ Fine-tune time will scale with dataset size. For <1000 samples, CPU is sufficient

### 🔌 API Reference

```POST /predict```

**Request:**
```json
{
  "text": "I love this!"
}
```
**Response:**
```json
{
  "label": "positive",
  "score": 0.9823
}
```