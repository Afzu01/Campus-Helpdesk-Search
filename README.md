# Campus Helpdesk Search

A lightweight campus support search application that retrieves relevant answers from a structured FAQ knowledge base and ranks them using TF-IDF and cosine similarity.

<p align="center">
  <strong>Ask a campus question. Get ranked, department-aware answers.</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white" alt="Python" />
  <img src="https://img.shields.io/badge/FastAPI-API-009688?logo=fastapi&logoColor=white" alt="FastAPI" />
  <img src="https://img.shields.io/badge/scikit--learn-TF--IDF-F7931E?logo=scikitlearn&logoColor=white" alt="scikit-learn" />
  <img src="https://img.shields.io/badge/Interface-HTML%20%2F%20CSS%20%2F%20JS-E34F26?logo=html5&logoColor=white" alt="Frontend" />
  <img src="https://img.shields.io/badge/Status-Prototype-orange" alt="Prototype" />
</p>

---

## Overview

Campus Helpdesk Search is a student-facing prototype for finding answers to common academic and administrative questions. Instead of manually browsing multiple departments or FAQ pages, a student can enter a natural-language query and receive the closest matching FAQ entries.

The project combines a **FastAPI backend**, a **TF-IDF retrieval pipeline**, a **CSV-based FAQ dataset**, and a small browser interface.

> **Retrieval note:** The current implementation uses TF-IDF vectors and cosine similarity. This is lexical similarity-based retrieval, not a transformer-based semantic search or embedding model.

## Features

- **Ranked FAQ retrieval** — compares a query against FAQ questions and answers.
- **Department context** — each result includes its owning department.
- **Configurable result count** — return between 1 and 20 results.
- **Minimum-score filtering** — hide results below a chosen cosine-similarity threshold.
- **Vector preview endpoint** — inspect the first 12 values of the query's TF-IDF vector.
- **Browser interface** — search and inspect results at `/ui`.
- **Interactive API documentation** — explore endpoints through FastAPI's Swagger UI.

## How it works

```text
Student query
     |
     v
Text preprocessing + TF-IDF vectorization
     |
     v
Cosine similarity against FAQ vectors
     |
     v
Rank results by similarity score
     |
     v
Apply minimum-score threshold + top-k limit
     |
     v
Return answers with department metadata
```

At application startup, the FAQ CSV is loaded, question and answer text are combined, and a TF-IDF matrix is built. Each incoming query is transformed with the same fitted vectorizer. Cosine similarity scores are then used to rank the FAQ entries.

## Technology stack

| Layer | Tools |
|---|---|
| Language | Python |
| API | FastAPI, Pydantic |
| Data handling | pandas, NumPy |
| Retrieval | scikit-learn TF-IDF, cosine similarity |
| Frontend | HTML, CSS, JavaScript |
| Data source | CSV |

## Project structure

```text
Campus-Helpdesk-Search/
├── app/
│   └── main.py              # FastAPI app and retrieval logic
├── data/
│   └── helpdesk_faq.csv     # Campus FAQ knowledge base
├── ui/
│   └── index.html           # Browser-based search interface
├── requirements.txt
├── run_demo.ps1
├── start_demo.bat
└── README.md
```

## Getting started

### 1. Clone the repository

```bash
git clone https://github.com/Afzu01/Campus-Helpdesk-Search.git
cd Campus-Helpdesk-Search
```

### 2. Create and activate a virtual environment

**Windows PowerShell**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install dependencies

```bash
python -m pip install -r requirements.txt
```

### 4. Start the API

```bash
uvicorn app.main:app --reload --port 8102
```

### 5. Open the application

| Resource | URL |
|---|---|
| Search interface | http://127.0.0.1:8102/ui |
| API documentation | http://127.0.0.1:8102/docs |
| Root endpoint | http://127.0.0.1:8102/ |

## API reference

### `POST /search`

Search the FAQ knowledge base and return ranked matches.

**Request**

```json
{
  "query": "how can I get a transcript?",
  "top_k": 3,
  "min_score": 0.1
}
```

| Parameter | Type | Default | Constraints |
|---|---|---:|---|
| `query` | string | Required | At least 2 characters |
| `top_k` | integer | 5 | 1–20 |
| `min_score` | float | 0.1 | 0.0–1.0 |

**Example response**

```json
{
  "query": "how can I get a transcript?",
  "count": 1,
  "results": [
    {
      "id": 6,
      "question": "How to request transcript copies?",
      "answer": "Raise transcript request and pay processing fee through accounts section.",
      "department": "admin",
      "score": 0.42
    }
  ]
}
```

*The score above is illustrative; actual scores depend on the query and dataset.*

### `POST /embed`

Returns the dimensionality of the query's TF-IDF representation and a preview of its first 12 values.

**Request**

```json
{
  "query": "hostel room change",
  "top_k": 1,
  "min_score": 0.0
}
```

**Response shape**

```json
{
  "dimensions": 000,
  "preview": [0.0, 0.0, 0.0]
}
```

The dimension count and vector values depend on the fitted vocabulary. This endpoint exposes a sparse text-feature representation converted to a dense array for preview; it does not generate neural embeddings.

## Dataset

The included `data/helpdesk_faq.csv` contains **30 sample FAQ records** across campus functions such as:

- Academics
- Administration
- IT
- Hostel
- Library
- Finance
- Placements
- Student welfare
- Health
- Sports

The records are demonstration data. They should be replaced or validated against an institution's official policies before real-world deployment.

## Current scope and limitations

This is a working prototype intended to demonstrate API development and information retrieval fundamentals.

- TF-IDF relies on token overlap; it may miss paraphrases that use different vocabulary.
- Similarity scores are ranking signals, not calibrated confidence or factuality probabilities.
- The FAQ dataset is small and illustrative.
- There is no authentication, user-specific access control, ticket creation, or production monitoring.
- The current data pipeline loads the CSV and builds the vectorizer when the application starts.

## Potential next steps

- Evaluate retrieval quality with a labelled query test set and metrics such as Precision@k and Recall@k.
- Compare TF-IDF with sentence-transformer embeddings and vector search.
- Add FAQ source links, freshness metadata, and an editorial workflow.
- Add automated tests, input/error handling, and deployment configuration.
- Introduce feedback capture so unanswered questions can improve the knowledge base.

## Run a quick test

With the server running, use:

```bash
curl -X POST "http://127.0.0.1:8102/search" \
  -H "Content-Type: application/json" \
  -d '{"query":"how to request transcript","top_k":3,"min_score":0.1}'
```

---

## Author

**Afzal Hussain**  
BSc (Hons) Data Science & AI | AI, data systems, and applied machine learning

- GitHub: [@Afzu01](https://github.com/Afzu01)

---

<p align="center">
  <sub>Built as a hands-on project in API engineering, text retrieval, and practical data science.</sub>
</p>
