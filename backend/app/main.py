import os
from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analyze import router as analyze_router

load_dotenv()

app = FastAPI(title="YouTube Feedback Intelligence API", version="0.1.0")
origin = os.getenv("FRONTEND_ORIGIN", "http://localhost:3000")
 
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "http://192.168.1.107:3000",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def health_check():
    return {"status": "ok", "message": "YouTube Feedback Intelligence API"}

app.include_router(analyze_router)
