from pathlib import Path

import pandas as pd
from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

DATA_FILE = Path(__file__).resolve().parent.parent / "data" / "helpdesk_faq.csv"
UI_FILE = Path(__file__).resolve().parent.parent / "ui" / "index.html"


class SearchRequest(BaseModel):
    query: str = Field(..., min_length=2)
    top_k: int = Field(default=5, ge=1, le=20)
    min_score: float = Field(default=0.1, ge=0.0, le=1.0)


faq_df = pd.read_csv(DATA_FILE)
faq_df["text"] = faq_df["question"].fillna("") + " " + faq_df["answer"].fillna("")
vectorizer = TfidfVectorizer(stop_words="english")
matrix = vectorizer.fit_transform(faq_df["text"])

app = FastAPI(title="Campus Helpdesk Search", version="1.0.0")


@app.get("/")
def root() -> dict:
    return {"message": "Campus Helpdesk Search", "docs": "/docs", "ui": "/ui"}


@app.get("/ui")
def ui() -> FileResponse:
    return FileResponse(UI_FILE)


@app.post("/search")
def search(payload: SearchRequest) -> dict:
    qvec = vectorizer.transform([payload.query])
    scores = cosine_similarity(qvec, matrix).flatten()
    ranked = scores.argsort()[::-1]

    results = []
    for idx in ranked:
        score = float(scores[idx])
        if score < payload.min_score:
            continue
        row = faq_df.iloc[idx]
        results.append(
            {
                "id": int(row["id"]),
                "question": row["question"],
                "answer": row["answer"],
                "department": row["department"],
                "score": round(score, 4),
            }
        )
        if len(results) >= payload.top_k:
            break

    return {"query": payload.query, "count": len(results), "results": results}


@app.post("/embed")
def embed(payload: SearchRequest) -> dict:
    vec = vectorizer.transform([payload.query]).toarray()[0]
    return {"dimensions": len(vec), "preview": vec[:12].tolist()}
