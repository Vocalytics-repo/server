from fastapi import APIRouter, HTTPException, Query
from typing import Optional
from .insight_service import InsightService

router = APIRouter(prefix="/api/insights", tags=["insights"])

# InsightService 인스턴스 생성
try:
    insight_service = InsightService()
except Exception as e:
    print(f"InsightService 초기화 실패: {e}")
    insight_service = None

@router.get("/gender-performance")
async def get_gender_performance(
    level: Optional[str] = Query(None, description="레벨 필터 (예: A, B, C)"),
    nationality: Optional[str] = Query(None, description="국적 필터 (예: Chinese)")
):
    """
    성별별 발음 성과 분석 API
    
    - 남성 vs 여성의 평균 오류율 비교
    - 성별별 CSID 오류 패턴 분포
    - 성별별 레벨 분포 및 진도 차이
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_gender_performance(level=level, nationality=nationality)
        return {
            "success": True,
            "data": result,
            "message": "성별별 발음 성과 분석이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/nationality-analysis")
async def get_nationality_analysis():
    """
    국적별 발음 특성 분석 API (전체 국적 비교)
    
    - 국적별 평균 오류율 및 표준편차
    - 국적별 CSID 오류 유형 선호도
    - 국적별 성과 랭킹
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_nationality_performance()
        return {
            "success": True,
            "data": result,
            "message": "국적별 발음 특성 분석이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/nationality-analysis/{nationality}")
async def get_specific_nationality_analysis(nationality: str):
    """
    특정 국적 발음 특성 분석 API
    
    - 특정 국적의 상세 발음 분석
    - 해당 국적이 어려워하는 한국어 패턴
    - 공통 오류 패턴 TOP 10
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_nationality_performance(nationality=nationality)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return {
            "success": True,
            "data": result,
            "message": f"'{nationality}' 국적의 발음 특성 분석이 완료되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/level-performance")
async def get_level_performance():
    """
    레벨별 성과 분석 API (전체 레벨 비교)
    
    - 레벨별 평균 오류율 및 분포
    - 레벨 상승에 따른 오류 패턴 변화
    - 학습 진도 트렌드 분석
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_level_performance()
        return {
            "success": True,
            "data": result,
            "message": "레벨별 성과 분석이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/level-performance/{level}")
async def get_specific_level_performance(level: str):
    """
    특정 레벨 성과 분석 API
    
    - 특정 레벨의 상세 성과 분석
    - 해당 레벨의 CSID 분포
    - 평균/중간값 오류율
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_level_performance(level=level)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return {
            "success": True,
            "data": result,
            "message": f"레벨 '{level}'의 성과 분석이 완료되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/csid-patterns")
async def get_csid_patterns(
    sex: Optional[str] = Query(None, description="성별 필터 (M/F)"),
    nationality: Optional[str] = Query(None, description="국적 필터"),
    level: Optional[str] = Query(None, description="레벨 필터")
):
    """
    CSID 오류 패턴 분석 API
    
    - C, S, I, D 비율 및 분포 분석
    - 그룹별 오류 유형 선호도
    - 정확도 및 오류 분포 계산
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_csid_patterns(sex=sex, nationality=nationality, level=level)
        
        if "error" in result:
            raise HTTPException(status_code=404, detail=result["error"])
        
        return {
            "success": True,
            "data": result,
            "message": "CSID 오류 패턴 분석이 완료되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/type-performance")
async def get_type_performance():
    """
    타입별 (String vs Word) 성과 분석 API
    
    - S타입 vs W타입 평균 오류율 비교
    - 타입별 CSID 패턴 차이
    - 문자열/단어 단위 학습 효과 분석
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.analyze_type_performance()
        return {
            "success": True,
            "data": result,
            "message": "타입별 성과 분석이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/text-difficulty")
async def get_text_difficulty(
    limit: int = Query(20, description="반환할 텍스트 개수 (기본값: 20)")
):
    """
    참조 텍스트 난이도 분석 API
    
    - ref별 평균 오류율 순위
    - 가장 어려운/쉬운 한국어 표현 TOP N
    - 텍스트 길이와 난이도 상관관계
    - 난이도별 분포 분석
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    if limit <= 0 or limit > 100:
        raise HTTPException(status_code=400, detail="limit은 1-100 사이의 값이어야 합니다.")
    
    try:
        result = insight_service.analyze_text_difficulty(limit=limit)
        return {
            "success": True,
            "data": result,
            "message": "참조 텍스트 난이도 분석이 완료되었습니다."
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/overview")
async def get_overview():
    """
    전체 지표 개요 API
    
    - 주요 KPI (평균 오류율, 전체 정확도, 샘플 수)
    - 상위 3개 오류 패턴
    - 성별/국적/레벨/타입별 요약 통계
    - 가장 어려운 텍스트 TOP 3
    - 핵심 인사이트 및 권장사항
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    try:
        result = insight_service.get_overview()
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        return {
            "success": True,
            "data": result,
            "message": "전체 지표 개요 분석이 완료되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/pronunciation-errors")
async def get_pronunciation_errors(
    ref_text: str = Query(..., description="분석할 참조 텍스트 (예: '시계', '안녕하세요')"),
    limit: int = Query(50, description="반환할 최대 문서 수 (기본값: 50)")
):
    """
    발음 오류 분석 API
    
    - 특정 단어/문장에 대한 발음 오류 패턴 분석
    - 정답 발음(ans), 인식된 발음(rec), 오류 설명(error) 제공
    - 성별/국적/레벨별 해당 텍스트 발음 성과 비교
    - 주요 오류 패턴 및 인사이트 제공
    """
    if not insight_service:
        raise HTTPException(status_code=500, detail="InsightService가 초기화되지 않았습니다.")
    
    if limit <= 0 or limit > 200:
        raise HTTPException(status_code=400, detail="limit은 1-200 사이의 값이어야 합니다.")
    
    try:
        result = insight_service.analyze_pronunciation_errors(ref_text=ref_text, limit=limit)
        
        if "error" in result:
            raise HTTPException(status_code=400, detail=result["error"])
        
        if result.get("found_documents", 0) == 0:
            return {
                "success": True,
                "data": result,
                "message": f"'{ref_text}'와 관련된 발음 데이터를 찾을 수 없습니다."
            }
        
        return {
            "success": True,
            "data": result,
            "message": f"'{ref_text}'에 대한 발음 오류 분석이 완료되었습니다."
        }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"분석 중 오류가 발생했습니다: {str(e)}")

@router.get("/health")
async def health_check():
    """
    인사이트 서비스 상태 확인 API
    """
    if not insight_service:
        return {
            "success": False,
            "message": "InsightService가 초기화되지 않았습니다.",
            "elasticsearch_connected": False
        }
    
    try:
        # Elasticsearch 연결 상태 확인
        es_connected = insight_service.es.ping()
        return {
            "success": True,
            "message": "인사이트 서비스가 정상적으로 작동 중입니다.",
            "elasticsearch_connected": es_connected,
            "index_name": insight_service.index_name
        }
    except Exception as e:
        return {
            "success": False,
            "message": f"서비스 상태 확인 중 오류가 발생했습니다: {str(e)}",
            "elasticsearch_connected": False
        } 