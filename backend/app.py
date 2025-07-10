from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from model import load_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sentiment_pipeline = load_model()

#Allow frontend ruuning at port 5173 and 3000
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text:str

@app.post("/predict")
def predict_sentiment(req: PredictRequest):
    print("predicting...")  # debug text

    if not req.text.strip():
        raise HTTPException(status_code=400, detail="Text input is empty")

    result = sentiment_pipeline(req.text)[0]

    label_map = {
        "POS": "positive",
        "NEU": "neutral",
        "NEG": "negative"
    }

    raw_label = result["label"].upper()
    mapped_label = label_map.get(raw_label, raw_label.lower())  # fallback in case of weird label

    return {
        "label": mapped_label,
        "score": round(result["score"], 4)
    }