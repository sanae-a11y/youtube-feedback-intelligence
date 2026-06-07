# 💖 YouTube Feedback Intelligence

An AI-powered pastel dashboard that transforms YouTube comments and transcripts into creator insights using LLMs.

![YouTube Feedback Intelligence](./youtube%20feedback%20intelligence.png)

---

## ✨ Features

* 💬 YouTube comment analysis
* 📈 Audience sentiment visualization
* 🧠 AI-generated creator insights
* 🎥 Next video recommendations
* 🌸 Aesthetic pastel dashboard
* ⚡ FastAPI + Next.js architecture
* 🤖 OpenRouter / Qwen LLM integration

---

## 🛠️ Tech Stack

### Frontend

* Next.js
* TailwindCSS
* Recharts
* TypeScript

### Backend

* FastAPI
* Python
* OpenRouter API
* YouTube Data API

### AI Models

* Qwen
* DeepSeek
* OpenRouter

---

## 📸 Demo

Paste a YouTube URL and get:

* audience sentiment
* best parts of the video
* improvement suggestions
* viewer requests
* next video ideas

---

## 🚀 Local Setup

### Backend

```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

Create `.env`:

```env
YOUTUBE_API_KEY=your_key
LLM_PROVIDER=openrouter
OPENROUTER_API_KEY=your_key
OPENROUTER_MODEL=deepseek/deepseek-chat-v3-0324:free
```

---

### Frontend

```bash
cd frontend
npm install
npm run dev
```

Create `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
```

---

## 🌍 Deployment

### Frontend

Deploy on Vercel.

### Backend

Deploy on Render.

---

## 💡 Future Improvements

* thumbnail analysis
* competitor analysis
* viral prediction
* automatic script generation
* multilingual analytics

---

## 👩‍💻 Author

Built with 💖 by Sanae Attak
