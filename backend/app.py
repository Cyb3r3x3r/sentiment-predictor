from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from model import load_model
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()
sentiment_pipeline = load_model()

#Allow frontend ruuning at vite port(5173)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class PredictRequest(BaseModel):
    text:str

@app.post("/predict")
def predict_sentiment(req: PredictRequest):
    # print("predicting...")       debug text
    if not req.text.strip():
        raise HTTPException(status_code=400,detail="Text input is empty")
    result = sentiment_pipeline(req.text)[0]
    return {
        "label":result["label"].lower(),
        "score":round(result["score"],4)
    }