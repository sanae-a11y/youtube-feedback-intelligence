import json
import os
import requests
from typing import Dict, Any, List

SYSTEM_PROMPT = """
You are an AI product analyst for YouTube creators. Return ONLY valid JSON.
Analyze comments and transcript to identify audience sentiment, loved parts, weaknesses, requests, and next-video ideas.
Use this exact schema:
{
  "sentiment": {"positive": 0, "neutral": 0, "negative": 0},
  "best_parts": ["..."],
  "improvements": ["..."],
  "viewer_requests": ["..."],
  "next_video_ideas": [{"title": "...", "why": "...", "confidence": 0}],
  "creator_advice": "..."
}
Percentages must sum to 100. Confidence is 0-100.
"""

def _safe_json(text: str) -> Dict[str, Any]:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("Model did not return JSON")
    return json.loads(text[start:end+1])

def build_user_prompt(title: str, description: str, transcript: str, comments: List[str]) -> str:
    comments_text = "\n".join([f"- {c}" for c in comments[:150]])
    transcript_short = transcript[:8000] if transcript else "Transcript unavailable."
    description_short = description[:1500]
    return f"""
Video title: {title}
Description: {description_short}
Transcript: {transcript_short}
Comments:
{comments_text}

Generate practical creator insights. Focus on what to improve and what next video should be.
"""

def call_ollama(prompt: str) -> Dict[str, Any]:
    base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
    model = os.getenv("OLLAMA_MODEL", "qwen2.5:7b")
    response = requests.post(
        f"{base_url}/api/chat",
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "stream": False,
            "format": "json",
        },
        timeout=120,
    )
    response.raise_for_status()
    content = response.json()["message"]["content"]
    return _safe_json(content)

def call_openrouter(prompt: str) -> Dict[str, Any]:
    api_key = os.getenv("OPENROUTER_API_KEY")
    if not api_key:
        raise RuntimeError("Missing OPENROUTER_API_KEY")
    model = os.getenv("OPENROUTER_MODEL", "qwen/qwen-2.5-7b-instruct:free")
    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"},
        json={
            "model": model,
            "messages": [
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": prompt},
            ],
            "response_format": {"type": "json_object"},
        },
        timeout=120,
    )
    response.raise_for_status()
    return _safe_json(response.json()["choices"][0]["message"]["content"])

def analyze_with_llm(title: str, description: str, transcript: str, comments: List[str]) -> Dict[str, Any]:
    prompt = build_user_prompt(title, description, transcript, comments)
    provider = os.getenv("LLM_PROVIDER", "ollama").lower()
    if provider == "openrouter":
        return call_openrouter(prompt)
    return call_ollama(prompt)
