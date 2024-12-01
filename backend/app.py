import logging
from config import Config
from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv
from utils.init_vector_store import initialize_vector_store
from utils.custom_chat_chains import (
    visibility_chain,
    comparison_chain,
    trend_chain,
    emerging_competitors_chain,
    crisis_analysis_chain,
    audience_segmentation_chain,
    competitive_benchmarking_chain,
    brand_health_score_chain,
    regional_trends_chain,
    self_representation_chain,
    gpt_perception_chain,
    self_vs_gpt_comparison_chain,
    brand_ranking_chain,
)
from models.input_models import (
    BrandRequest,
    BrandComparisonRequest,
    TrendRequest,
    RegionalTrendRequest,
    BrandRequestWithIndustry,
    CompetitiveBenchmarkingRequest,
    MultiTopicRequest,
    BrandRankingRequest,
)
from models.output_models import (
    BrandVisibilityResponse,
    BrandComparisonResponse,
    BrandTrendsResponse,
    EmergingCompetitorsResponse,
    CrisisAnalysisResponse,
    AudienceSegmentationResponse,
    CompetitiveBenchmarkingResponse,
    BrandHealthScoreResponse,
    RegionalTrendsResponse,
    SelfRepresentationResponse,
    GPTPerceptionResponse,
    SelfVsGPTResponse,
    BrandRankingResponse,
)

# Load environment variables
load_dotenv()

# Initialize vector store
vector_store_manager = initialize_vector_store()

# Initialize FastAPI app
app = FastAPI()

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.Logging.LEVEL.upper(), logging.INFO),
    format=Config.Logging.FORMAT,
)
logger = logging.getLogger("brand_analysis_api")


# APIs

@app.post("/brand/visibility", response_model=BrandVisibilityResponse)
async def api_get_brand_visibility(request: BrandRequest):
    """
    Get brand visibility details.
    """
    try:
        logger.info(f"Received request for brand visibility: {request.brand_name}")
        response = visibility_chain.invoke(brand_name=request.brand_name)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing visibility request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process brand visibility analysis")


@app.post("/brand/comparison", response_model=BrandComparisonResponse)
async def api_compare_brands(request: BrandComparisonRequest):
    """
    Compare two brands.
    """
    try:
        logger.info(f"Received request to compare brands: {request.brand1} and {request.brand2}")
        response = comparison_chain.invoke(brand1=request.brand1, brand2=request.brand2)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing comparison request between {request.brand1} and {request.brand2}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process brand comparison")


@app.post("/brand/trends", response_model=BrandTrendsResponse)
async def api_get_brand_trends(request: TrendRequest):
    """
    Get brand trends and emerging topics.
    """
    try:
        logger.info(f"Received request for brand trends: {request.brand_name} over {request.time_period}")
        response = trend_chain.invoke(brand_name=request.brand_name, time_period=request.time_period)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing trends request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process brand trends analysis")


@app.post("/brand/emerging_competitors", response_model=EmergingCompetitorsResponse)
async def api_get_emerging_competitors(request: BrandRequestWithIndustry):
    """
    Get emerging competitors for a brand.
    """
    try:
        logger.info(f"Received request for emerging competitors: {request.brand_name} in industry: {request.industry}")
        response = emerging_competitors_chain.invoke(brand_name=request.brand_name, industry=request.industry)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing emerging competitors request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process emerging competitors analysis")


@app.post("/brand/crisis_analysis", response_model=CrisisAnalysisResponse)
async def api_get_crisis_analysis(request: TrendRequest):
    """
    Analyze crises or negative trends affecting a brand.
    """
    try:
        logger.info(f"Received request for crisis analysis: {request.brand_name} over {request.time_period}")
        response = crisis_analysis_chain.invoke(brand_name=request.brand_name, time_period=request.time_period)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing crisis analysis request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process crisis analysis")


@app.post("/brand/audience_segmentation", response_model=AudienceSegmentationResponse)
async def api_get_audience_segmentation(request: TrendRequest):
    """
    Get audience segmentation insights.
    """
    try:
        logger.info(f"Received request for audience segmentation: {request.brand_name} over {request.time_period}")
        response = audience_segmentation_chain.invoke(brand_name=request.brand_name, time_period=request.time_period)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing audience segmentation request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process audience segmentation")


@app.post("/brand/competitive_benchmarking", response_model=CompetitiveBenchmarkingResponse)
async def api_get_competitive_benchmarking(request: CompetitiveBenchmarkingRequest):
    """
    Get competitive benchmarking insights.
    """
    try:
        logger.info(f"Received request for competitive benchmarking: {request.brand_name} with competitors {request.competitors}")
        response = competitive_benchmarking_chain.invoke(
            brand_name=request.brand_name,
            competitors=request.competitors,
            time_period=request.time_period
        )
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing competitive benchmarking: {e}")
        raise HTTPException(status_code=500, detail="Failed to process competitive benchmarking")


@app.post("/brand/health_score", response_model=BrandHealthScoreResponse)
async def api_get_brand_health_score(request: BrandRequest):
    """
    Get brand health score.
    """
    try:
        logger.info(f"Received request for brand health score: {request.brand_name}")
        response = brand_health_score_chain.invoke(brand_name=request.brand_name)
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing brand health score: {e}")
        raise HTTPException(status_code=500, detail="Failed to process brand health score")


@app.post("/brand/regional_trends", response_model=RegionalTrendsResponse)
async def api_get_regional_trends(request: RegionalTrendRequest):
    """
    Get regional trends.
    """
    try:
        logger.info(f"Received request for regional trends: {request.brand_name} in {request.time_period}")
        response = regional_trends_chain.invoke(
            brand_name=request.brand_name,
            region=request.region,
            time_period=request.time_period
        )
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing regional trends: {e}")
        raise HTTPException(status_code=500, detail="Failed to process regional trends")


@app.post("/brand/self_representation", response_model=SelfRepresentationResponse)
async def api_get_self_representation(request: MultiTopicRequest):
    """
    Analyze a brand's self-representation.
    """
    try:
        logger.info(f"Analyzing self-representation for {request.brand_name} on topics: {request.topics}")
        documents = vector_store_manager.retrieve_documents_by_topics(request.brand_name, request.topics)
        response = self_representation_chain.invoke(
            brand_name=request.brand_name,
            topics=request.topics,
            retrieved_documents="\n".join([doc.page_content for doc in documents]),
        )
        return response
    except Exception as e:
        logger.error(f"Error processing self-representation request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process self-representation analysis")


@app.post("/brand/gpt_perception", response_model=GPTPerceptionResponse)
async def api_get_gpt_perception(request: MultiTopicRequest):
    """
    Analyze GPT's perception of a brand.
    """
    try:
        logger.info(f"Analyzing GPT perception for {request.brand_name} on topics: {request.topics}")
        documents = vector_store_manager.retrieve_documents_by_topics(request.brand_name, request.topics)
        response = gpt_perception_chain.invoke(
            brand_name=request.brand_name,
            topics=request.topics,
            retrieved_documents=documents,
        )
        return response
    except Exception as e:
        logger.error(f"Error processing GPT perception request for {request.brand_name}: {e}")
        raise HTTPException(status_code=500, detail="Failed to process GPT perception analysis")


@app.post("/brand/self_vs_gpt", response_model=SelfVsGPTResponse)
async def api_self_vs_gpt(request: MultiTopicRequest):
    """
    Compare a brand's self-representation with GPT's perception.
    """
    try:
        logger.info(f"Received request for self vs GPT analysis: {request.brand_name} on topics: {request.topics}")
        
        documents = vector_store_manager.retrieve_documents_by_topics(request.brand_name, topics=request.topics)
        if not documents:
            logger.error(f"No relevant documents found for {request.brand_name}. Skipping.")
            
        response = self_vs_gpt_comparison_chain.invoke(
            brand_name=request.brand_name,
            retrieved_documents=documents,
            topics=request.topics
        )
        if response:
            return response
    except Exception as e:
        logger.error(f"Error processing self vs GPT analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to process self vs GPT analysis")


@app.post("/brand/self_representation_ranking")#, response_model=BrandSelfRepresentationRankingResponse
async def api_rank_brands_by_self_representation(request: BrandRankingRequest):
    """
    Rank brands based on self-representation across a set of topics.
    """
    try:
        logger.info(f"Ranking brands based on self-representation: {request.brands}")
        brand_scores = []

        for brand_name in request.brands:
            try:
                documents = vector_store_manager.retrieve_documents_by_topics(brand_name, topics=request.topics)
                if not documents:
                    logger.warning(f"No relevant documents found for {brand_name}. Skipping.")
                    continue

                response = self_representation_chain.invoke(
                    brand_name=brand_name,
                    retrieved_documents=documents,
                    topics=request.topics,
                )
                brand_scores.append({
                    "brand_name": brand_name,
                    "score": response.self_representation_score,
                    "insights": response.insights,
                })

            except Exception as e:
                logger.error(f"Error evaluating self-representation for {brand_name}: {e}")

        ranked_brands = sorted(brand_scores, key=lambda x: x["score"], reverse=True)
        return {"ranked_brands": ranked_brands}
    except Exception as e:
        logger.error(f"Error processing self-representation ranking: {e}")
        raise HTTPException(status_code=500, detail="Failed to process self-representation ranking")


@app.post("/brand/rankings", response_model=BrandRankingResponse)
async def api_rank_brands(request: BrandRankingRequest):
    """
    Rank brands based on their performance across multiple topics.
    """
    try:
        logger.info(f"Received request to rank brands: {request.brands} for topics: {request.topics}")
        all_documents = []
        
        for brand in request.brands:
            documents = vector_store_manager.retrieve_documents_by_topics(brand, request.topics)
            if documents:
                all_documents.append({
                    "brand": brand,
                    "documents": "\n".join([doc.page_content for doc in documents])
                })
            else:
                logger.warning(f"No relevant documents found for {brand}")

        response = brand_ranking_chain.invoke(
            brands=request.brands,
            topics=request.topics,
            retrieved_documents=all_documents
        )

        if response:
            logger.info(f"Ranking response: {response}")
            return response.dict()
        else:
            raise ValueError("Chain did not return a response.")

    except Exception as e:
        logger.error(f"Error processing brand rankings: {e}")
        return {"error": "Failed to process brand rankings"}