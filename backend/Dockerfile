# Stage 1: Download the model
FROM python:3.10-slim AS downloader

WORKDIR /download

RUN pip install --no-cache-dir transformers torch==2.1.2+cpu --extra-index-url https://download.pytorch.org/whl/cpu

RUN python3 -c "\
from transformers import pipeline; \
pipe = pipeline('sentiment-analysis', model='mrm8488/deberta-v3-small-finetuned-sst2'); \
pipe.model.save_pretrained('/download/model'); \
pipe.tokenizer.save_pretrained('/download/model')"

# Stage 2: Final image
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

COPY --from=downloader /download/model ./model

EXPOSE 8000

CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
