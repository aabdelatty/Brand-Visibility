import logging
from config import Config
from utils.vstore import VectorStoreManager

def initialize_vector_store():
    """
    Initialize the Vector Store Manager by scraping websites and building indices for each brand.
    """

    # Set up logging using the configuration
    logging.basicConfig(
        level=getattr(logging, Config.Logging.LEVEL.upper(), logging.INFO),
        format=Config.Logging.FORMAT,
        handlers=[
            logging.StreamHandler(),
        ]
    )

    logging.info("Initializing Vector Store...")
    manager = VectorStoreManager()

    # List of brand data with name and website URL
    brand_data = Config.VectorStore.BRAND_DATA
    
    # Loop through each brand and build indices
    for brand in brand_data:
        logging.info(f"Processing brand: {brand['name']}")
        try:
            manager.build_indices_for_brand(brand["url"], brand["name"])
            logging.info(f"Indices built for brand: {brand['name']}")
        except Exception as e:
            logging.error(f"Failed to process brand {brand['name']}: {e}")
            
    return manager

# if __name__ == "__main__":
#     initialize_vector_store()
