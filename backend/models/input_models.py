from pydantic import BaseModel
from typing import List


class BrandRequest(BaseModel):
    brand_name: str


class BrandRequestWithIndustry(BaseModel):
    brand_name: str
    industry: str


class BrandComparisonRequest(BaseModel):
    brand1: str
    brand2: str


class TrendRequest(BaseModel):
    brand_name: str
    time_period: str


class RegionalTrendRequest(BaseModel):
    brand_name: str
    region: str
    time_period: str
    
class CompetitiveBenchmarkingRequest(BaseModel):
    brand_name: str
    competitors: List[str]
    time_period: str


class MultiTopicRequest(BaseModel):
    brand_name: str
    topics: List[str]


class BrandRankingRequest(BaseModel):
    brands: List[str]
    topics: List[str]
