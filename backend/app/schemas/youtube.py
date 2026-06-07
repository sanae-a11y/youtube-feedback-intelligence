from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict, Any

class AnalyzeRequest(BaseModel):
    url: HttpUrl
    language: str = "en"
    max_comments: int = 120

class VideoMetadata(BaseModel):
    video_id: str
    title: str = ""
    description: str = ""
    channel_title: str = ""
    published_at: str = ""
    thumbnail_url: str = ""
    view_count: int = 0
    like_count: int = 0
    comment_count: int = 0

class ExtractResponse(BaseModel):
    metadata: VideoMetadata
    transcript: str
    comments: List[str]

class AnalysisResponse(BaseModel):
    metadata: VideoMetadata
    sentiment: Dict[str, float]
    best_parts: List[str]
    improvements: List[str]
    viewer_requests: List[str]
    next_video_ideas: List[Dict[str, Any]]
    creator_advice: str
    raw_comment_count: int
    transcript_available: bool
