from elasticsearch import Elasticsearch
from typing import Dict, List, Any, Optional
import os
from dotenv import load_dotenv
from collections import defaultdict, Counter
import statistics

# 환경변수 로드
load_dotenv()

class InsightService:
    def __init__(self):
        es_url = os.getenv("ELASTICSEARCH_URL")
        es_username = os.getenv("ES_USERNAME")
        es_password = os.getenv("ES_PASSWORD")
        self.index_name = os.getenv("ELASTICSEARCH_INDEX_NAME")
        
        if not all([es_url, es_username, es_password, self.index_name]):
            raise ValueError("필수 환경변수가 설정되지 않았습니다.")
        
        self.es = Elasticsearch(es_url, basic_auth=(es_username, es_password))
        
        if not self.es.ping():
            raise ConnectionError("Elasticsearch 연결에 실패했습니다.")
    
    def _execute_search(self, query: Dict) -> List[Dict]:
        """Elasticsearch 검색 실행"""
        try:
            response = self.es.search(index=self.index_name, body=query)
            return response['hits']['hits']
        except Exception as e:
            print(f"검색 실행 오류: {e}")
            return []
    
    def _get_all_data(self, filters: Optional[Dict] = None) -> List[Dict]:
        """모든 데이터 조회 (필터 적용 가능)"""
        query = {
            "query": {
                "match_all": {}
            },
            "size": 10000  # 최대 10,000개 문서 조회
        }
        
        if filters:
            must_clauses = []
            for field, value in filters.items():
                if value is not None:
                    must_clauses.append({"term": {field: value}})
            
            if must_clauses:
                query["query"] = {
                    "bool": {
                        "must": must_clauses
                    }
                }
        
        hits = self._execute_search(query)
        return [hit['_source'] for hit in hits]
    
    def analyze_gender_performance(self, level: Optional[str] = None, nationality: Optional[str] = None) -> Dict[str, Any]:
        """성별별 발음 성과 분석"""
        filters = {}
        if level:
            filters['level'] = level
        if nationality:
            filters['nationality'] = nationality
        
        data = self._get_all_data(filters)
        
        male_data = [d for d in data if d.get('sex') == 'M']
        female_data = [d for d in data if d.get('sex') == 'F']
        
        def calculate_stats(gender_data):
            if not gender_data:
                return {
                    "count": 0,
                    "avg_error_rate": 0,
                    "csid_distribution": {"C": 0, "S": 0, "I": 0, "D": 0},
                    "level_distribution": {}
                }
            
            error_rates = [d.get('per', 0) for d in gender_data if d.get('per') is not None]
            csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
            level_counts = Counter()
            
            for d in gender_data:
                for key in csid_totals:
                    csid_totals[key] += d.get(key, 0)
                level_counts[d.get('level')] += 1
            
            return {
                "count": len(gender_data),
                "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                "median_error_rate": statistics.median(error_rates) if error_rates else 0,
                "std_error_rate": statistics.stdev(error_rates) if len(error_rates) > 1 else 0,
                "csid_distribution": csid_totals,
                "level_distribution": dict(level_counts)
            }
        
        male_stats = calculate_stats(male_data)
        female_stats = calculate_stats(female_data)
        
        return {
            "male": male_stats,
            "female": female_stats,
            "comparison": {
                "error_rate_difference": male_stats["avg_error_rate"] - female_stats["avg_error_rate"],
                "total_samples": male_stats["count"] + female_stats["count"]
            }
        }
    
    def analyze_nationality_performance(self, nationality: Optional[str] = None) -> Dict[str, Any]:
        """국적별 발음 특성 분석"""
        data = self._get_all_data()
        
        if nationality:
            # 특정 국적 분석
            nationality_data = [d for d in data if d.get('nationality') == nationality]
            
            if not nationality_data:
                return {"error": f"국적 '{nationality}' 데이터를 찾을 수 없습니다."}
            
            error_rates = [d.get('per', 0) for d in nationality_data if d.get('per') is not None]
            csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
            level_counts = Counter()
            error_patterns = Counter()
            
            for d in nationality_data:
                for key in csid_totals:
                    csid_totals[key] += d.get(key, 0)
                level_counts[d.get('level')] += 1
                if d.get('error'):
                    error_patterns[d.get('error')] += 1
            
            return {
                "nationality": nationality,
                "count": len(nationality_data),
                "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                "median_error_rate": statistics.median(error_rates) if error_rates else 0,
                "csid_distribution": csid_totals,
                "level_distribution": dict(level_counts),
                "common_errors": dict(error_patterns.most_common(10))
            }
        else:
            # 모든 국적 비교 분석
            nationality_stats = defaultdict(lambda: {
                "data": [],
                "csid_totals": {"C": 0, "S": 0, "I": 0, "D": 0}
            })
            
            for d in data:
                nat = d.get('nationality')
                if nat:
                    nationality_stats[nat]["data"].append(d)
                    for key in nationality_stats[nat]["csid_totals"]:
                        nationality_stats[nat]["csid_totals"][key] += d.get(key, 0)
            
            result = {}
            for nat, stats in nationality_stats.items():
                error_rates = [d.get('per', 0) for d in stats["data"] if d.get('per') is not None]
                result[nat] = {
                    "count": len(stats["data"]),
                    "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                    "csid_distribution": stats["csid_totals"]
                }
            
            # 국적별 성과 랭킹
            sorted_nationalities = sorted(result.items(), key=lambda x: x[1]["avg_error_rate"])
            
            return {
                "nationality_stats": result,
                "ranking": {
                    "best_performance": sorted_nationalities[:3],
                    "worst_performance": sorted_nationalities[-3:]
                }
            }
    
    def analyze_level_performance(self, level: Optional[str] = None) -> Dict[str, Any]:
        """레벨별 성과 분석"""
        data = self._get_all_data()
        
        if level:
            # 특정 레벨 분석
            level_data = [d for d in data if d.get('level') == level]
            
            if not level_data:
                return {"error": f"레벨 '{level}' 데이터를 찾을 수 없습니다."}
            
            error_rates = [d.get('per', 0) for d in level_data if d.get('per') is not None]
            csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
            
            for d in level_data:
                for key in csid_totals:
                    csid_totals[key] += d.get(key, 0)
            
            return {
                "level": level,
                "count": len(level_data),
                "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                "median_error_rate": statistics.median(error_rates) if error_rates else 0,
                "csid_distribution": csid_totals
            }
        else:
            # 모든 레벨 비교 분석
            level_stats = defaultdict(lambda: {
                "data": [],
                "csid_totals": {"C": 0, "S": 0, "I": 0, "D": 0}
            })
            
            for d in data:
                lvl = d.get('level')
                if lvl:
                    level_stats[lvl]["data"].append(d)
                    for key in level_stats[lvl]["csid_totals"]:
                        level_stats[lvl]["csid_totals"][key] += d.get(key, 0)
            
            result = {}
            for lvl, stats in level_stats.items():
                error_rates = [d.get('per', 0) for d in stats["data"] if d.get('per') is not None]
                result[lvl] = {
                    "count": len(stats["data"]),
                    "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                    "median_error_rate": statistics.median(error_rates) if error_rates else 0,
                    "csid_distribution": stats["csid_totals"]
                }
            
            return {
                "level_stats": result,
                "progression_analysis": self._analyze_level_progression(result)
            }
    
    def _analyze_level_progression(self, level_stats: Dict) -> Dict[str, Any]:
        """레벨 진행에 따른 성과 변화 분석"""
        levels = sorted(level_stats.keys())
        error_rates = [level_stats[level]["avg_error_rate"] for level in levels]
        
        return {
            "levels": levels,
            "error_rate_trend": error_rates,
            "improvement_rate": error_rates[0] - error_rates[-1] if len(error_rates) > 1 else 0
        }
    
    def analyze_csid_patterns(self, sex: Optional[str] = None, nationality: Optional[str] = None, level: Optional[str] = None) -> Dict[str, Any]:
        """CSID 오류 패턴 분석"""
        filters = {}
        if sex:
            filters['sex'] = sex
        if nationality:
            filters['nationality'] = nationality
        if level:
            filters['level'] = level
        
        data = self._get_all_data(filters)
        
        if not data:
            return {"error": "조건에 맞는 데이터를 찾을 수 없습니다."}
        
        csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
        total_errors = 0
        
        for d in data:
            for key in csid_totals:
                value = d.get(key, 0)
                csid_totals[key] += value
                if key != "C":  # Correct는 오류가 아님
                    total_errors += value
        
        # 비율 계산
        total_operations = sum(csid_totals.values())
        csid_ratios = {}
        error_ratios = {}
        
        for key, value in csid_totals.items():
            csid_ratios[key] = (value / total_operations * 100) if total_operations > 0 else 0
            if key != "C":
                error_ratios[key] = (value / total_errors * 100) if total_errors > 0 else 0
        
        return {
            "sample_count": len(data),
            "csid_counts": csid_totals,
            "csid_ratios": csid_ratios,
            "error_distribution": error_ratios,
            "total_operations": total_operations,
            "total_errors": total_errors,
            "accuracy_rate": csid_ratios.get("C", 0)
        }
    
    def analyze_type_performance(self) -> Dict[str, Any]:
        """타입별 (String vs Word) 성과 분석"""
        data = self._get_all_data()
        
        string_data = [d for d in data if d.get('type') == 'S']
        word_data = [d for d in data if d.get('type') == 'W']
        
        def calculate_type_stats(type_data, type_name):
            if not type_data:
                return {
                    "type": type_name,
                    "count": 0,
                    "avg_error_rate": 0,
                    "csid_distribution": {"C": 0, "S": 0, "I": 0, "D": 0}
                }
            
            error_rates = [d.get('per', 0) for d in type_data if d.get('per') is not None]
            csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
            
            for d in type_data:
                for key in csid_totals:
                    csid_totals[key] += d.get(key, 0)
            
            return {
                "type": type_name,
                "count": len(type_data),
                "avg_error_rate": statistics.mean(error_rates) if error_rates else 0,
                "median_error_rate": statistics.median(error_rates) if error_rates else 0,
                "csid_distribution": csid_totals
            }
        
        string_stats = calculate_type_stats(string_data, "String")
        word_stats = calculate_type_stats(word_data, "Word")
        
        return {
            "string_analysis": string_stats,
            "word_analysis": word_stats,
            "comparison": {
                "error_rate_difference": string_stats["avg_error_rate"] - word_stats["avg_error_rate"],
                "better_performance": "String" if string_stats["avg_error_rate"] < word_stats["avg_error_rate"] else "Word",
                "total_samples": string_stats["count"] + word_stats["count"]
            }
        }
    
    def analyze_text_difficulty(self, limit: int = 20) -> Dict[str, Any]:
        """참조 텍스트 난이도 분석"""
        data = self._get_all_data()
        
        text_stats = defaultdict(lambda: {
            "error_rates": [],
            "count": 0,
            "csid_totals": {"C": 0, "S": 0, "I": 0, "D": 0}
        })
        
        for d in data:
            ref_text = d.get('ref')
            if ref_text:
                text_stats[ref_text]["error_rates"].append(d.get('per', 0))
                text_stats[ref_text]["count"] += 1
                for key in text_stats[ref_text]["csid_totals"]:
                    text_stats[ref_text]["csid_totals"][key] += d.get(key, 0)
        
        # 통계 계산
        text_difficulty = {}
        for text, stats in text_stats.items():
            if stats["count"] >= 2:  # 최소 2개 이상의 샘플이 있는 텍스트만
                error_rates = stats["error_rates"]
                text_difficulty[text] = {
                    "text": text,
                    "sample_count": stats["count"],
                    "avg_error_rate": statistics.mean(error_rates),
                    "median_error_rate": statistics.median(error_rates),
                    "std_error_rate": statistics.stdev(error_rates) if len(error_rates) > 1 else 0,
                    "text_length": len(text),
                    "csid_distribution": stats["csid_totals"]
                }
        
        # 난이도별 정렬
        sorted_by_difficulty = sorted(text_difficulty.values(), key=lambda x: x["avg_error_rate"], reverse=True)
        
        return {
            "total_unique_texts": len(text_difficulty),
            "hardest_texts": sorted_by_difficulty[:limit],
            "easiest_texts": sorted_by_difficulty[-limit:],
            "difficulty_distribution": {
                "very_hard": len([t for t in text_difficulty.values() if t["avg_error_rate"] > 0.3]),
                "hard": len([t for t in text_difficulty.values() if 0.2 < t["avg_error_rate"] <= 0.3]),
                "medium": len([t for t in text_difficulty.values() if 0.1 < t["avg_error_rate"] <= 0.2]),
                "easy": len([t for t in text_difficulty.values() if t["avg_error_rate"] <= 0.1])
            }
        }
    
    def get_overview(self) -> Dict[str, Any]:
        """전체 지표 개요 - 주요 KPI와 인사이트를 한눈에 제공"""
        data = self._get_all_data()
        
        if not data:
            return {"error": "분석할 데이터가 없습니다."}
        
        # 기본 통계
        total_samples = len(data)
        error_rates = [d.get('per', 0) for d in data if d.get('per') is not None]
        overall_avg_error_rate = statistics.mean(error_rates) if error_rates else 0
        
        # CSID 전체 통계
        csid_totals = {"C": 0, "S": 0, "I": 0, "D": 0}
        for d in data:
            for key in csid_totals:
                csid_totals[key] += d.get(key, 0)
        
        total_operations = sum(csid_totals.values())
        overall_accuracy = (csid_totals["C"] / total_operations * 100) if total_operations > 0 else 0
        
        # 상위 3개 오류 패턴
        error_patterns = Counter()
        for d in data:
            if d.get('error'):
                error_patterns[d.get('error')] += 1
        top_error_patterns = dict(error_patterns.most_common(3))
        
        # 성별별 요약
        male_data = [d for d in data if d.get('sex') == 'M']
        female_data = [d for d in data if d.get('sex') == 'F']
        
        male_error_rates = [d.get('per', 0) for d in male_data if d.get('per') is not None]
        female_error_rates = [d.get('per', 0) for d in female_data if d.get('per') is not None]
        
        gender_summary = {
            "male": {
                "count": len(male_data),
                "avg_error_rate": statistics.mean(male_error_rates) if male_error_rates else 0
            },
            "female": {
                "count": len(female_data),
                "avg_error_rate": statistics.mean(female_error_rates) if female_error_rates else 0
            }
        }
        
        # 국적별 요약 (상위 5개)
        nationality_stats = defaultdict(lambda: {"data": [], "error_rates": []})
        for d in data:
            nat = d.get('nationality')
            if nat:
                nationality_stats[nat]["data"].append(d)
                if d.get('per') is not None:
                    nationality_stats[nat]["error_rates"].append(d.get('per', 0))
        
        nationality_summary = {}
        for nat, stats in nationality_stats.items():
            if stats["error_rates"]:
                nationality_summary[nat] = {
                    "count": len(stats["data"]),
                    "avg_error_rate": statistics.mean(stats["error_rates"])
                }
        
        # 성과 순으로 정렬하여 상위 5개만
        top_nationalities = dict(sorted(nationality_summary.items(), 
                                      key=lambda x: x[1]["avg_error_rate"])[:5])
        
        # 레벨별 요약
        level_stats = defaultdict(lambda: {"data": [], "error_rates": []})
        for d in data:
            lvl = d.get('level')
            if lvl:
                level_stats[lvl]["data"].append(d)
                if d.get('per') is not None:
                    level_stats[lvl]["error_rates"].append(d.get('per', 0))
        
        level_summary = {}
        for lvl, stats in level_stats.items():
            if stats["error_rates"]:
                level_summary[lvl] = {
                    "count": len(stats["data"]),
                    "avg_error_rate": statistics.mean(stats["error_rates"])
                }
        
        # 타입별 요약
        string_data = [d for d in data if d.get('type') == 'S']
        word_data = [d for d in data if d.get('type') == 'W']
        
        string_error_rates = [d.get('per', 0) for d in string_data if d.get('per') is not None]
        word_error_rates = [d.get('per', 0) for d in word_data if d.get('per') is not None]
        
        type_summary = {
            "string": {
                "count": len(string_data),
                "avg_error_rate": statistics.mean(string_error_rates) if string_error_rates else 0
            },
            "word": {
                "count": len(word_data),
                "avg_error_rate": statistics.mean(word_error_rates) if word_error_rates else 0
            }
        }
        
        # 가장 어려운 텍스트 TOP 3
        text_stats = defaultdict(lambda: {"error_rates": [], "count": 0})
        for d in data:
            ref_text = d.get('ref')
            if ref_text and d.get('per') is not None:
                text_stats[ref_text]["error_rates"].append(d.get('per', 0))
                text_stats[ref_text]["count"] += 1
        
        text_difficulty = []
        for text, stats in text_stats.items():
            if stats["count"] >= 2:  # 최소 2개 이상의 샘플
                avg_error_rate = statistics.mean(stats["error_rates"])
                text_difficulty.append({
                    "text": text,
                    "avg_error_rate": avg_error_rate,
                    "sample_count": stats["count"]
                })
        
        hardest_texts = sorted(text_difficulty, key=lambda x: x["avg_error_rate"], reverse=True)[:3]
        
        # 주요 인사이트 생성
        insights = []
        
        # 성별 인사이트
        if gender_summary["male"]["count"] > 0 and gender_summary["female"]["count"] > 0:
            male_rate = gender_summary["male"]["avg_error_rate"]
            female_rate = gender_summary["female"]["avg_error_rate"]
            if abs(male_rate - female_rate) > 0.02:  # 2% 이상 차이
                better_gender = "여성" if female_rate < male_rate else "남성"
                insights.append(f"{better_gender}이 평균적으로 더 좋은 발음 성과를 보입니다.")
        
        # 타입 인사이트
        if type_summary["string"]["count"] > 0 and type_summary["word"]["count"] > 0:
            string_rate = type_summary["string"]["avg_error_rate"]
            word_rate = type_summary["word"]["avg_error_rate"]
            if abs(string_rate - word_rate) > 0.02:
                better_type = "단어 단위" if word_rate < string_rate else "문자열 단위"
                insights.append(f"{better_type} 학습이 더 효과적입니다.")
        
        # 오류율 인사이트
        if overall_avg_error_rate > 0.15:
            insights.append("전체적으로 오류율이 높아 추가적인 학습 지원이 필요합니다.")
        elif overall_avg_error_rate < 0.05:
            insights.append("전체적으로 매우 우수한 발음 성과를 보이고 있습니다.")
        
        return {
            "summary": {
                "total_samples": total_samples,
                "overall_avg_error_rate": overall_avg_error_rate,
                "overall_accuracy": overall_accuracy,
                "data_coverage": {
                    "nationalities": len(nationality_summary),
                    "levels": len(level_summary),
                    "unique_texts": len(text_stats)
                }
            },
            "csid_overview": {
                "totals": csid_totals,
                "ratios": {
                    "C": (csid_totals["C"] / total_operations * 100) if total_operations > 0 else 0,
                    "S": (csid_totals["S"] / total_operations * 100) if total_operations > 0 else 0,
                    "I": (csid_totals["I"] / total_operations * 100) if total_operations > 0 else 0,
                    "D": (csid_totals["D"] / total_operations * 100) if total_operations > 0 else 0
                }
            },
            "top_error_patterns": top_error_patterns,
            "gender_summary": gender_summary,
            "nationality_summary": top_nationalities,
            "level_summary": level_summary,
            "type_summary": type_summary,
            "hardest_texts": hardest_texts,
            "key_insights": insights
        } 