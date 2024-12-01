import os
import pathlib
from dataclasses import dataclass
from dotenv import load_dotenv

load_dotenv()

root_path = pathlib.Path(__file__).parent



@dataclass(init=False)
class Config:

    class Logging:
        """
        Configuration for logging settings.
        """
        LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
        FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"

    class Paths:
        """
        Configuration for file paths.
        """
        DATA_DIR = os.environ.get("DATA_DIR", "data")
        SCRAPED_DATA_TEMPLATE = os.path.join(DATA_DIR, "{brand_name}_scraped_data.json")
        PROMPT_BASE_PATH = os.environ.get("PROMPT_BASE_PATH", "prompt_templates")
        VISIBILITY_ANALYSIS = os.path.join(PROMPT_BASE_PATH, "visibility_analysis.yaml")
        COMPARISON_ANALYSIS = os.path.join(PROMPT_BASE_PATH, "comparison_analysis.yaml")
        TREND_ANALYSIS = os.path.join(PROMPT_BASE_PATH, "trend_analysis.yaml")
        EMERGING_COMPETITORS = os.path.join(PROMPT_BASE_PATH, "emerging_competitors.yaml")
        CRISIS_ANALYSIS = os.path.join(PROMPT_BASE_PATH, "crisis_analysis.yaml")
        AUDIENCE_SEGMENTATION = os.path.join(PROMPT_BASE_PATH, "audience_segmentation.yaml")
        COMPETITIVE_BENCHMARKING = os.path.join(PROMPT_BASE_PATH, "competitive_benchmarking.yaml")
        BRAND_HEALTH_SCORE = os.path.join(PROMPT_BASE_PATH, "brand_health_score.yaml")
        REGIONAL_TRENDS = os.path.join(PROMPT_BASE_PATH, "regional_trends.yaml")
        SELF_REPRESENTATION = os.path.join(PROMPT_BASE_PATH, "self_representation.yaml")
        GPT_PERCEPTION = os.path.join(PROMPT_BASE_PATH, "gpt_perception.yaml")
        SELF_VS_GPT_COMPARISON = os.path.join(PROMPT_BASE_PATH, "self_vs_gpt_comparison.yaml")
        Brand_Ranking = os.path.join(PROMPT_BASE_PATH, "brand_ranking.yaml")

    class OpenAI:
        """
        Configuration for OpenAI settings.
        """
        API_KEY = os.getenv("OPENAI_API_KEY")
        MODEL_NAME = os.environ.get("OPENAI_MODEL", "gpt-4o")
        TIMEOUT = int(os.environ.get("OPENAI_TIMEOUT", 30))
        TEMPERATURE = float(os.environ.get("OPENAI_TEMPERATURE", 0.3))
        EMBEDDING_MODEL = os.environ.get("OPENAI_EMBEDDING_MODEL", "text-embedding-ada-002")

    class Scraper:
        """
        Configuration for web scraping settings.
        """
        MAX_DEPTH = int(os.environ.get("SCRAPER_MAX_DEPTH", 2))


    class VectorStore:
        """
        Configuration for vector store management.
        """
        BRAND_DATA = [
            {"name": "Ally", "url": "https://www.ally.com/"},
            {"name": "Chime", "url": "https://www.chime.com/"},
            {"name": "VaroMoney", "url": "https://www.varomoney.com/"},
            {"name": "CapitalOne", "url": "https://www.capitalone.com/"},
        ]
