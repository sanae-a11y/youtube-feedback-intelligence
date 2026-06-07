from fastapi import APIRouter, HTTPException
from app.schemas.youtube import AnalyzeRequest, ExtractResponse, AnalysisResponse
from app.services.youtube_service import extract_video_data
from app.services.llm_service import analyze_with_llm

router = APIRouter(prefix="/api", tags=["youtube-analysis"])

@router.post("/extract", response_model=ExtractResponse)
def extract(request: AnalyzeRequest):
    try:
        metadata, transcript, comments = extract_video_data(str(request.url), request.language, request.max_comments)
        return ExtractResponse(metadata=metadata, transcript=transcript, comments=comments)
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/analyze", response_model=AnalysisResponse)
def analyze(request: AnalyzeRequest):
    try:
        metadata, transcript, comments = extract_video_data(str(request.url), request.language, request.max_comments)
        result = analyze_with_llm(metadata.title, metadata.description, transcript, comments)
        return AnalysisResponse(
            metadata=metadata,
            sentiment=result.get("sentiment", {"positive": 0, "neutral": 0, "negative": 0}),
            best_parts=result.get("best_parts", []),
            improvements=result.get("improvements", []),
            viewer_requests=result.get("viewer_requests", []),
            next_video_ideas=result.get("next_video_ideas", []),
            creator_advice=result.get("creator_advice", ""),
            raw_comment_count=len(comments),
            transcript_available=bool(transcript),
        )
    except Exception as exc:
        raise HTTPException(status_code=400, detail=str(exc))
