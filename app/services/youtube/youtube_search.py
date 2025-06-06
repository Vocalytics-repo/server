import os
from typing import List, Dict, Optional
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

class YouTubeSearchService:
    def __init__(self):
        self.api_key = os.getenv("GOOGLE_API_KEY")
        if not self.api_key:
            raise ValueError("GOOGLE_API_KEY 환경변수가 설정되지 않았습니다.")
        
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)
    
    def search_videos(
        self, 
        query: str, 
        max_results: int = 10,
        order: str = "relevance",
        region_code: str = "KR",
        relevance_language: str = "ko"
    ) -> List[Dict]:
        """
        YouTube에서 영상을 검색합니다.
        
        Args:
            query: 검색어
            max_results: 최대 결과 수 (기본값: 10)
            order: 정렬 방식 (relevance, date, rating, viewCount, title)
            region_code: 지역 코드 (기본값: KR)
            relevance_language: 관련성 언어 (기본값: ko)
        
        Returns:
            검색된 영상 정보 리스트
        """
        try:
            # YouTube Data API v3 검색 요청
            search_response = self.youtube.search().list(
                q=query,
                part='id,snippet',
                maxResults=max_results,
                order=order,
                regionCode=region_code,
                relevanceLanguage=relevance_language,
                type='video',
                videoEmbeddable='true',  # 임베드 가능한 영상만
                videoSyndicated='true'   # 신디케이션 가능한 영상만
            ).execute()
            
            videos = []
            for search_result in search_response.get('items', []):
                video_id = search_result['id']['videoId']
                snippet = search_result['snippet']
                
                video_info = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail_url': snippet['thumbnails']['medium']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'embed_url': f"https://www.youtube.com/embed/{video_id}"
                }
                videos.append(video_info)
            
            logger.info(f"검색어 '{query}'에 대해 {len(videos)}개의 영상을 찾았습니다.")
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API 오류: {e}")
            if e.resp.status == 403:
                raise HTTPException(
                    status_code=403, 
                    detail="YouTube API 할당량이 초과되었거나 API 키가 유효하지 않습니다."
                )
            elif e.resp.status == 400:
                raise HTTPException(
                    status_code=400,
                    detail="잘못된 검색 요청입니다."
                )
            else:
                raise HTTPException(
                    status_code=500,
                    detail=f"YouTube API 오류가 발생했습니다: {str(e)}"
                )
        except Exception as e:
            logger.error(f"예상치 못한 오류: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"영상 검색 중 오류가 발생했습니다: {str(e)}"
            )
    
    def get_video_details(self, video_ids: List[str]) -> List[Dict]:
        """
        영상 ID 리스트로 상세 정보를 가져옵니다.
        
        Args:
            video_ids: 영상 ID 리스트
        
        Returns:
            영상 상세 정보 리스트
        """
        try:
            video_response = self.youtube.videos().list(
                part='snippet,statistics,contentDetails',
                id=','.join(video_ids)
            ).execute()
            
            videos = []
            for video in video_response.get('items', []):
                video_id = video['id']
                snippet = video['snippet']
                statistics = video.get('statistics', {})
                content_details = video.get('contentDetails', {})
                
                video_info = {
                    'video_id': video_id,
                    'title': snippet['title'],
                    'description': snippet['description'],
                    'channel_title': snippet['channelTitle'],
                    'published_at': snippet['publishedAt'],
                    'thumbnail_url': snippet['thumbnails']['medium']['url'],
                    'video_url': f"https://www.youtube.com/watch?v={video_id}",
                    'embed_url': f"https://www.youtube.com/embed/{video_id}",
                    'view_count': statistics.get('viewCount', '0'),
                    'like_count': statistics.get('likeCount', '0'),
                    'duration': content_details.get('duration', 'PT0S')
                }
                videos.append(video_info)
            
            return videos
            
        except HttpError as e:
            logger.error(f"YouTube API 오류: {e}")
            raise HTTPException(
                status_code=500,
                detail=f"영상 상세 정보를 가져오는 중 오류가 발생했습니다: {str(e)}"
            )

# 싱글톤 인스턴스
youtube_service = None

def get_youtube_service() -> YouTubeSearchService:
    """YouTube 서비스 인스턴스를 반환합니다."""
    global youtube_service
    if youtube_service is None:
        youtube_service = YouTubeSearchService()
    return youtube_service 