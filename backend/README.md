# Backend

## Setup

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

Add your YouTube API key in `.env`.

For local free LLM:

```bash
ollama pull qwen2.5:7b
ollama run qwen2.5:7b
```

Run API:

```bash
uvicorn app.main:app --reload --port 8000
```
