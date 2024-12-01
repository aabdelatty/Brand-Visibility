from pydantic import BaseModel, Field
from typing import List, Dict


class SentimentDistribution(BaseModel):
    positive: int = Field(..., description="Percentage of positive sentiment.")
    neutral: int = Field(..., description="Percentage of neutral sentiment.")
    negative: int = Field(..., description="Percentage of negative sentiment.")


class BrandVisibilityResponse(BaseModel):
    visibility_score: int = Field(..., description="Visibility score of the brand (0-100).")
    key_sentiments: SentimentDistribution = Field(..., description="Sentiment distribution for the brand.")
    top_topics: List[str] = Field(..., description="Top 3 topics related to the brand.")
    top_regions: List[str] = Field(..., description="Top 3 regions where the brand is most visible.")


class BrandComparisonResponse(BaseModel):
    brand1_visibility: int = Field(..., description="Visibility score for Brand 1.")
    brand2_visibility: int = Field(..., description="Visibility score for Brand 2.")
    differentiators: List[str] = Field(..., description="Key differences between the two brands.")


class TrendTopic(BaseModel):
    topic: str = Field(..., description="Trending topic related to the brand.")
    sentiment_score: int = Field(..., description="Sentiment score (0-100) for the topic.")


class BrandTrendsResponse(BaseModel):
    trending_topics: List[TrendTopic] = Field(..., description="List of trending topics.")
    emerging_regions: List[str] = Field(..., description="Regions where the brand is gaining visibility.")


class EmergingCompetitor(BaseModel):
    name: str = Field(..., description="Name of the competitor.")
    growth_rate: float = Field(..., description="Growth rate of the competitor in percentage.")
    differentiators: List[str] = Field(..., description="List of differentiators for the competitor.")


class EmergingCompetitorsResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    competitors: List[EmergingCompetitor] = Field(..., description="List of emerging competitors.")


class CrisisAnalysisResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    time_period: str = Field(..., description="The time period for the analysis.")
    negative_trends: List[str] = Field(..., description="List of top negative trends impacting the brand.")
    root_causes: List[str] = Field(..., description="List of root causes for the negative trends.")
    recommendations: List[str] = Field(..., description="Suggested strategies for mitigating the issues.")


class AudienceSegment(BaseModel):
    demographics: Dict[str, str] = Field(..., description="Key demographic attributes such as age, gender, and location.")
    preferences: List[str] = Field(..., description="List of preferences and interests of the segment.")
    engagement_patterns: Dict[str, int] = Field(..., description="Engagement patterns such as 'social_media' and 'reviews' percentages.")


class AudienceSegmentationResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    key_segments: List[AudienceSegment] = Field(..., description="List of audience segments.")


class CompetitiveBenchmarkingResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the primary brand being analyzed.")
    competitors: List[str] = Field(..., description="List of competitors being compared.")
    visibility_scores: Dict[str, int] = Field(..., description="Visibility scores for each brand.")
    sentiment_distributions: Dict[str, Dict[str, int]] = Field(..., description="Sentiment distribution for each brand.")
    key_differentiators: Dict[str, List[str]] = Field(..., description="Key differentiators for each brand.")


class BrandHealthScoreResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    health_score: int = Field(..., description="Overall health score of the brand (0-100).")
    industry_benchmark: int = Field(..., description="Average health score for the industry (0-100).")
    key_insights: List[str] = Field(..., description="Positive insights for the brand.")
    improvement_areas: List[str] = Field(..., description="Areas where the brand can improve.")


class RegionalTrendsResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    region: str = Field(..., description="Region for the analysis.")
    time_period: str = Field(..., description="Time period for the analysis.")
    key_trends: List[Dict[str, str]] = Field(..., description="List of key trends in the region.")
    recommendations: List[str] = Field(..., description="Suggestions to improve brand visibility or perception.")


class SelfRepresentationResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    topics: List[str] = Field(..., description="List of topics analyzed.")
    self_representation_score: int = Field(..., description="Self-representation score (0-100).")
    insights: List[str] = Field(..., description="Key insights from the analysis.")


class GPTPerceptionResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    topics: List[str] = Field(..., description="List of topics analyzed.")
    gpt_perception_score: int = Field(..., description="GPT perception score (0-100).")
    insights: List[str] = Field(..., description="Key insights from the analysis.")


class SelfVsGPTResponse(BaseModel):
    brand_name: str = Field(..., description="Name of the brand being analyzed.")
    topics: List[str] = Field(..., description="List of topics analyzed.")
    self_representation_score: int = Field(..., description="Self-representation score (0-100).")
    gpt_perception_score: int = Field(..., description="GPT perception score (0-100).")
    alignment_score: int = Field(..., description="Alignment score between self-representation and GPT perception (0-100).")
    discrepancies: List[str] = Field(..., description="Key discrepancies between self-representation and GPT perception.")


class RankedBrand(BaseModel):
    """
    Model for a ranked brand in self-representation ranking.
    """
    brand_name: str = Field(..., description="The name of the brand.")
    score: int = Field(..., description="The self-representation score of the brand (0-100).")
    insights: List[str] = Field(..., description="Key insights about the brand's self-representation.")
    top_topics: List[str] = Field(..., description="Top topics that contributed to the score.")
    areas_for_improvement: List[str] = Field(..., description="Key areas where the brand can improve its self-representation.")


class BrandSelfRepresentationRankingResponse(BaseModel):
    """
    Response model for ranking brands based on self-representation.
    """
    ranked_brands: List[RankedBrand] = Field(..., description="List of brands ranked by self-representation score.")
    average_score: float = Field(..., description="Average self-representation score across all brands.")
    highest_scoring_topic: str = Field(..., description="The topic with the highest average score across brands.")
    lowest_scoring_topic: str = Field(..., description="The topic with the lowest average score across brands.")
    
class AreaRanking(BaseModel):
    """
    Response model for ranking brands given a topic.
    """
    topic: str
    rankings: List[Dict[str, int]]  

class BrandRankingResponse(BaseModel):
    """
    Response model for ranking brands based per topic and overall ranking.
    """
    rankings: List[AreaRanking]
    overall_ranking: List[Dict[str, int]]