# Campus Helpdesk Search

A student-facing semantic helpdesk that helps users find the right campus process quickly.

## Portfolio pitch

A semantic self-service support layer that reduces repetitive helpdesk load and improves student response speed.

## Why this helps real users

- Reduces confusion around admin and academic processes
- Gives fast self-service answers before raising tickets
- Supports confidence filtering to avoid poor matches

## Features

- Semantic search endpoint with min-score threshold
- Embedding preview endpoint
- 30 realistic FAQ entries across campus departments
- Modern UI at `/ui`

## Architecture

- FastAPI backend with TF-IDF + cosine similarity retrieval
- Confidence thresholding to suppress weak matches
- CSV knowledge base seeded with cross-department FAQs
- Frontend search UI for instant ranked answers

## Run

```powershell
cd D:\Code\python\campus-helpdesk-search
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8102
```

- UI: http://127.0.0.1:8102/ui
- Docs: http://127.0.0.1:8102/docs

## API quick test

```powershell
Invoke-RestMethod -Method POST -Uri "http://127.0.0.1:8102/search" -ContentType "application/json" -Body '{"query":"how to request transcript","top_k":3,"min_score":0.15}'
```

## Recruiter demo points

1. Query: `how to get transcript copies`
2. Show department-tagged ranked results
3. Increase `min_score` and explain confidence filtering
4. Run `/embed` and explain vectorization for semantic retrieval

## Screenshots / Demo GIF

- Add semantic results screenshot (query + ranked cards)
- Optional: add short GIF showing min-score tuning effect
