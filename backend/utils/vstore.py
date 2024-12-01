import os
import json
import asyncio
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_text_splitters import HTMLHeaderTextSplitter
from langchain.docstore.document import Document as LangChainDocument
from utils.playwright_scraper import scrape_website_recursive

import logging
from config import Config
from dotenv import load_dotenv

# Set up logging using the configuration
logging.basicConfig(
    level=getattr(logging, Config.Logging.LEVEL.upper(), logging.INFO),
    format=Config.Logging.FORMAT,
    handlers=[
        logging.StreamHandler(),
    ]
)

load_dotenv()
os.environ["OPENAI_API_KEY"] = Config.OpenAI.API_KEY

embedding_model = OpenAIEmbeddings()

class VectorStoreManager:
    def __init__(self):
        self.vector_stores = {}

    def save_scraped_data(self, brand_name, scraped_data):
        file_name = Config.Paths.SCRAPED_DATA_TEMPLATE.format(brand_name=brand_name)
        os.makedirs(Config.Paths.DATA_DIR, exist_ok=True)
        with open(file_name, "w", encoding="utf-8") as file:
            json.dump(scraped_data, file, ensure_ascii=False, indent=4)
        logging.info(f"Saved scraped data for {brand_name} to {file_name}")

    def load_scraped_data(self, brand_name):
        file_name = Config.Paths.SCRAPED_DATA_TEMPLATE.format(brand_name=brand_name)
        if os.path.exists(file_name):
            with open(file_name, "r", encoding="utf-8") as file:
                logging.info(f"Loaded scraped data for {brand_name} from {file_name}")
                return json.load(file)
        return None

    def scrape_website_sync(self, brand_base_url):
        return asyncio.run(scrape_website_recursive(brand_base_url, max_depth=Config.Scraper.MAX_DEPTH))

    def build_indices_for_brand(self, brand_base_url, brand_name):
        if brand_name in self.vector_stores:
            logging.info(f"Indices for {brand_name} already exist. Skipping build.")
            return

        scraped_data = self.load_scraped_data(brand_name)
        if not scraped_data:
            logging.info(f"No saved data found for {brand_name}. Starting scraping.")
            scraped_data = self.scrape_website_sync(brand_base_url)
            self.save_scraped_data(brand_name, scraped_data)

        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
        title_documents = [
            LangChainDocument(page_content=data["title"], metadata={"url": data["url"], "name": brand_name})
            for data in scraped_data if data.get("title")
        ]
        content_documents = [
            LangChainDocument(page_content=chunk, metadata={"url": data["url"], "title": data["title"], "name": brand_name})
            for data in scraped_data if data.get("content")
            for chunk in text_splitter.split_text(data["content"])
        ]
        paragraphs_documents = [
            LangChainDocument(page_content=paragraph, metadata={"url": data["url"], "title": data["title"], "name": brand_name})
            for data in scraped_data if data.get("paragraphs")
            for paragraph in data["paragraphs"]
        ]

        # Build FAISS indices
        title_faiss_index = FAISS.from_documents(title_documents, embedding_model)
        content_faiss_index = FAISS.from_documents(content_documents, embedding_model)
        paragraphs_faiss_index = FAISS.from_documents(paragraphs_documents, embedding_model)

        # Store indices in memory
        self.vector_stores[brand_name] = {
            "title_index": title_faiss_index,
            "content_index": content_faiss_index,
            "paragraphs_index": paragraphs_faiss_index,
        }
        logging.info(f"Indices for {brand_name} built and stored.")

    def search_indices(self, brand_name, query, k_title=5, k_content=5):
        if brand_name not in self.vector_stores:
            logging.info(f"No indices found for {brand_name}. Building them.")
            raise ValueError(f"No indices for brand: {brand_name}")

        title_index = self.vector_stores[brand_name]["title_index"]
        paragraphs_index = self.vector_stores[brand_name]["paragraphs_index"]

        logging.info(f"Searching indices for {brand_name} with query: {query}")
        title_results = title_index.similarity_search(query, k=k_title)
        title_result_urls = {result.metadata["url"] for result in title_results}

        paragraphs_results = paragraphs_index.similarity_search(query, k=k_content, filter={"url": list(title_result_urls)})

        return "\n".join([result.page_content for result in paragraphs_results])

    def retrieve_documents_by_topics(self, brand_name, topics, k=5):
        if brand_name not in self.vector_stores:
            logging.error(f"No indices available for {brand_name}.")
            return []

        content_index = self.vector_stores[brand_name]["content_index"]
        results = []

        for topic in topics:
            topic_results = content_index.similarity_search(topic, k=k)
            results.extend(topic_results)

        return results
