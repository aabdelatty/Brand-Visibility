import os
import logging
from config import Config
from langchain.prompts import load_prompt
from langchain_core.output_parsers import JsonOutputParser
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from models.output_models import (
    BrandVisibilityResponse,
    BrandComparisonResponse,
    BrandTrendsResponse,
    EmergingCompetitorsResponse,
    CrisisAnalysisResponse,
    AudienceSegmentationResponse,
    CompetitiveBenchmarkingResponse,
    RegionalTrendsResponse,
    BrandHealthScoreResponse,
    SelfRepresentationResponse, 
    GPTPerceptionResponse, 
    SelfVsGPTResponse,
    BrandRankingResponse
)

# Load environment variables
load_dotenv()

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("chains")

# Load OpenAI API key from .env file
os.environ["OPENAI_API_KEY"] = Config.OpenAI.API_KEY
model_name = Config.OpenAI.MODEL_NAME
temperature = Config.OpenAI.TEMPERATURE

class custom_chat_chain:
    def __init__(self, pydantic_object, prompt):
        try:
            self.prompt = prompt
            self.pydantic_object = pydantic_object
            self.parser = JsonOutputParser(pydantic_object=pydantic_object)
            self.model = ChatOpenAI(
                temperature=temperature,
                model=model_name,
                verbose=True
            )
            self.chain = self.prompt | self.model.bind() | self.parser
            logger.info(f"CustomChatChain initialized successfully with {model_name}.")
        except Exception as e:
            logger.error(f"Error initializing CustomChatChain: {e}")

    def invoke(self, **kwargs):
        """
        Invoke the chain and log input/output.
        """
        try:
            # Generate format instructions dynamically
            format_instructions = self.parser.get_format_instructions()

            # Inject format_instructions into kwargs
            kwargs["format_instructions"] = format_instructions
            
            # Log the input to the chain
            logger.info(f"Invoking chain with input: {kwargs}")

            # Call the chain
            response = self.chain.invoke(kwargs)

            # Log the output of the chain
            logger.info(f"Chain output: {response}")
            

            return self.pydantic_object(**response)
        except Exception as e:
            logger.error(f"Error invoking chain with input {kwargs}: {e}")
            return None


# Loading prompt files using file paths from the configuration class
visibility_prompt = load_prompt(Config.Paths.VISIBILITY_ANALYSIS)
comparison_prompt = load_prompt(Config.Paths.COMPARISON_ANALYSIS)
trend_prompt = load_prompt(Config.Paths.TREND_ANALYSIS)
emerging_competitors_prompt = load_prompt(Config.Paths.EMERGING_COMPETITORS)
crisis_analysis_prompt = load_prompt(Config.Paths.CRISIS_ANALYSIS)
audience_segmentation_prompt = load_prompt(Config.Paths.AUDIENCE_SEGMENTATION)
competitive_benchmarking_prompt = load_prompt(Config.Paths.COMPETITIVE_BENCHMARKING)
brand_health_score_prompt = load_prompt(Config.Paths.BRAND_HEALTH_SCORE)
regional_trends_prompt = load_prompt(Config.Paths.REGIONAL_TRENDS)
self_representation_prompt = load_prompt(Config.Paths.SELF_REPRESENTATION)
gpt_perception_prompt = load_prompt(Config.Paths.GPT_PERCEPTION)
self_vs_gpt_comparison_prompt = load_prompt(Config.Paths.SELF_VS_GPT_COMPARISON)
brand_ranking_prompt = load_prompt(Config.Paths.Brand_Ranking)


# Chains for various functionalities
# Define chains
visibility_chain = custom_chat_chain(
    pydantic_object=BrandVisibilityResponse,
    prompt=visibility_prompt
)

comparison_chain = custom_chat_chain(
    pydantic_object=BrandComparisonResponse,
    prompt=comparison_prompt
)

trend_chain = custom_chat_chain(
    pydantic_object=BrandTrendsResponse,
    prompt=trend_prompt
)


emerging_competitors_chain = custom_chat_chain(
    pydantic_object=EmergingCompetitorsResponse,
    prompt=emerging_competitors_prompt
)

crisis_analysis_chain = custom_chat_chain(
    pydantic_object=CrisisAnalysisResponse,
    prompt=crisis_analysis_prompt
)

audience_segmentation_chain = custom_chat_chain(
    pydantic_object=AudienceSegmentationResponse,
    prompt=audience_segmentation_prompt
)


competitive_benchmarking_chain = custom_chat_chain(
    pydantic_object=CompetitiveBenchmarkingResponse,
    prompt=competitive_benchmarking_prompt
)

brand_health_score_chain = custom_chat_chain(
    pydantic_object=BrandHealthScoreResponse,
    prompt=brand_health_score_prompt
)

regional_trends_chain = custom_chat_chain(
    pydantic_object=RegionalTrendsResponse,
    prompt=regional_trends_prompt
)


self_representation_chain = custom_chat_chain(
    pydantic_object=SelfRepresentationResponse,
    prompt=self_representation_prompt
)

gpt_perception_chain = custom_chat_chain(
    pydantic_object=GPTPerceptionResponse,
    prompt=gpt_perception_prompt
)

self_vs_gpt_comparison_chain = custom_chat_chain(
    pydantic_object=SelfVsGPTResponse,
    prompt=self_vs_gpt_comparison_prompt
)

brand_ranking_chain = custom_chat_chain(
    pydantic_object=BrandRankingResponse,
    prompt=brand_ranking_prompt
)