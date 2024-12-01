import os
from dataclasses import dataclass

@dataclass(init=False)
class Config:
    """
    Centralized configuration for the Streamlit application.
    """
    class Logging:
        """
        Logging settings for Streamlit app.
        """
        LEVEL = os.environ.get("LOGGING_LEVEL", "INFO")
        FORMAT = "%(asctime)s [%(levelname)s] [%(filename)s:%(lineno)d] %(message)s"

    class Backend:
        """
        Backend API configuration.
        """
        URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

    class UI:
        """
        User interface configurations.
        """
        PAGE_TITLE = os.environ.get("UI_PAGE_TITLE", "Brand Analysis")
        LAYOUT = os.environ.get("UI_LAYOUT", "wide")

    class Data:
        """
        Predefined data for dropdowns and multi-selects.
        """
        BRANDS = [
            "Ally", "VaroMoney", "CapitalOne", "Chime"
        ]
        TOPICS = [
            "Customer Service", "Online Banking", "Mobile App Features", "Credit Card Rewards",
            "Loan Options", "Interest Rates", "ATM Accessibility", "Fraud Protection",
            "Sustainability", "Brand Reputation", "Investment Services"
        ]
        TIME_PERIODS = [
            "Last 1 month", "Last 3 months", "Last 6 months", "Last 12 months"
        ]
