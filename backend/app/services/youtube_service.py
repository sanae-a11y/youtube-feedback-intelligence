import os
import re
from typing import List, Tuple
from googleapiclient.discovery import build
from youtube_transcript_api import YouTubeTranscriptApi
from app.schemas.youtube import VideoMetadata

YOUTUBE_PATTERNS = [
    r"(?:v=)([a-zA-Z0-9_-]{11})",
    r"youtu\.be/([a-zA-Z0-9_-]{11})",
    r"youtube\.com/shorts/([a-zA-Z0-9_-]{11})",
    r"youtube\.com/embed/([a-zA-Z0-9_-]{11})",
]

def extract_video_id(url: str) -> str:
    for pattern in YOUTUBE_PATTERNS:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    raise ValueError("Invalid YouTube URL. Please paste a normal YouTube video, Shorts, or youtu.be link.")

def youtube_client():
    api_key = os.getenv("YOUTUBE_API_KEY")
    if not api_key:
        raise RuntimeError("Missing YOUTUBE_API_KEY. Add it to backend/.env")
    return build("youtube", "v3", developerKey=api_key)

def get_video_metadata(video_id: str) -> VideoMetadata:
    youtube = youtube_client()
    response = youtube.videos().list(part="snippet,statistics", id=video_id).execute()
    if not response.get("items"):
        raise ValueError("Video not found or unavailable.")
    item = response["items"][0]
    snippet = item.get("snippet", {})
    stats = item.get("statistics", {})
    thumbs = snippet.get("thumbnails", {})
    thumb = thumbs.get("high") or thumbs.get("medium") or thumbs.get("default") or {}
    return VideoMetadata(
        video_id=video_id,
        title=snippet.get("title", ""),
        description=snippet.get("description", ""),
        channel_title=snippet.get("channelTitle", ""),
        published_at=snippet.get("publishedAt", ""),
        thumbnail_url=thumb.get("url", ""),
        view_count=int(stats.get("viewCount", 0)),
        like_count=int(stats.get("likeCount", 0)),
        comment_count=int(stats.get("commentCount", 0)),
    )

def get_transcript(video_id: str, language: str = "en") -> str:
    try:
        transcript = YouTubeTranscriptApi.get_transcript(video_id, languages=[language, "en", "fr", "ar"])
        return " ".join([line.get("text", "") for line in transcript]).strip()
    except Exception:
        return ""

def get_comments(video_id: str, max_comments: int = 120) -> List[str]:
    youtube = youtube_client()
    comments: List[str] = []
    next_token = None
    while len(comments) < max_comments:
        response = youtube.commentThreads().list(
            part="snippet,replies",
            videoId=video_id,
            maxResults=min(100, max_comments - len(comments)),
            pageToken=next_token,
            textFormat="plainText",
            order="relevance",
        ).execute()
        for item in response.get("items", []):
            top = item["snippet"]["topLevelComment"]["snippet"].get("textDisplay", "")
            if top:
                comments.append(top)
            for reply in item.get("replies", {}).get("comments", []):
                txt = reply.get("snippet", {}).get("textDisplay", "")
                if txt and len(comments) < max_comments:
                    comments.append(txt)
        next_token = response.get("nextPageToken")
        if not next_token:
            break
    return comments[:max_comments]

def extract_video_data(url: str, language: str = "en", max_comments: int = 120) -> Tuple[VideoMetadata, str, List[str]]:
    video_id = extract_video_id(url)
    metadata = get_video_metadata(video_id)
    transcript = get_transcript(video_id, language)
    comments = get_comments(video_id, max_comments)
    return metadata, transcript, comments
