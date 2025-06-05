from fastapi import APIRouter, Query, HTTPException
from typing import List, Dict, Optional
from pydantic import BaseModel
from .youtube_search import get_youtube_service
import logging

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/youtube", tags=["YouTube"])

class VideoSearchRequest(BaseModel):
    query: str
    max_results: Optional[int] = 10
    order: Optional[str] = "relevance"
    region_code: Optional[str] = "KR"
    relevance_language: Optional[str] = "ko"

class VideoInfo(BaseModel):
    video_id: str
    title: str
    description: str
    channel_title: str
    published_at: str
    thumbnail_url: str
    video_url: str
    embed_url: str

class VideoSearchResponse(BaseModel):
    success: bool
    message: str
    data: List[VideoInfo]
    total_results: int

@router.post("/search", response_model=VideoSearchResponse)
async def search_videos(request: VideoSearchRequest):
    """
    YouTube에서 영상을 검색합니다.
    
    - **query**: 검색어 (필수)
    - **max_results**: 최대 결과 수 (기본값: 10, 최대: 50)
    - **order**: 정렬 방식 (relevance, date, rating, viewCount, title)
    - **region_code**: 지역 코드 (기본값: KR)
    - **relevance_language**: 관련성 언어 (기본값: ko)
    """
    try:
        # 최대 결과 수 제한
        if request.max_results > 50:
            request.max_results = 50
        
        youtube_service = get_youtube_service()
        videos = youtube_service.search_videos(
            query=request.query,
            max_results=request.max_results,
            order=request.order,
            region_code=request.region_code,
            relevance_language=request.relevance_language
        )
        
        return VideoSearchResponse(
            success=True,
            message=f"'{request.query}' 검색 결과를 성공적으로 가져왔습니다.",
            data=videos,
            total_results=len(videos)
        )
        
    except Exception as e:
        logger.error(f"영상 검색 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/search", response_model=VideoSearchResponse)
async def search_videos_get(
    query: str = Query(..., description="검색어"),
    max_results: int = Query(10, description="최대 결과 수", le=50),
    order: str = Query("relevance", description="정렬 방식"),
    region_code: str = Query("KR", description="지역 코드"),
    relevance_language: str = Query("ko", description="관련성 언어")
):
    """
    GET 방식으로 YouTube에서 영상을 검색합니다.
    
    예시: /youtube/search?query=한국어 초급자를 위한 교육 영상&max_results=10
    """
    try:
        youtube_service = get_youtube_service()
        videos = youtube_service.search_videos(
            query=query,
            max_results=max_results,
            order=order,
            region_code=region_code,
            relevance_language=relevance_language
        )
        
        return VideoSearchResponse(
            success=True,
            message=f"'{query}' 검색 결과를 성공적으로 가져왔습니다.",
            data=videos,
            total_results=len(videos)
        )
        
    except Exception as e:
        logger.error(f"영상 검색 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/video/{video_id}")
async def get_video_details(video_id: str):
    """
    특정 영상의 상세 정보를 가져옵니다.
    """
    try:
        youtube_service = get_youtube_service()
        videos = youtube_service.get_video_details([video_id])
        
        if not videos:
            raise HTTPException(status_code=404, detail="영상을 찾을 수 없습니다.")
        
        return {
            "success": True,
            "message": "영상 정보를 성공적으로 가져왔습니다.",
            "data": videos[0]
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"영상 상세 정보 조회 오류: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/health")
async def health_check():
    """
    YouTube 서비스 상태를 확인합니다.
    """
    try:
        youtube_service = get_youtube_service()
        return {
            "success": True,
            "message": "YouTube 서비스가 정상적으로 작동 중입니다.",
            "service": "YouTube Data API v3"
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"YouTube 서비스 오류: {str(e)}",
            "service": "YouTube Data API v3"
        } 