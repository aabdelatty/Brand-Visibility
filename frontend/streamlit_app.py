import streamlit as st
import requests
import logging
from config import Config

# Set up logging
logging.basicConfig(
    level=getattr(logging, Config.Logging.LEVEL.upper(), logging.INFO),
    format=Config.Logging.FORMAT,
)
logger = logging.getLogger("StreamlitApp")

# Use backend URL from Config
BACKEND_URL = Config.Backend.URL

banking_brands = Config.Data.BRANDS
banking_topics = Config.Data.TOPICS
time_periods = Config.Data.TIME_PERIODS

# Set the Streamlit page configuration
st.set_page_config(
    page_title=Config.UI.PAGE_TITLE,
    layout=Config.UI.LAYOUT
)

# Header for the app
st.title(Config.UI.PAGE_TITLE)
st.write(
    """
    This tool provides comprehensive analysis and insights into brand visibility, trends, and competitive benchmarking.
    Utilize APIs to extract actionable insights and evaluate brand performance across various dimensions.
    """
)

# Main Tabs for broader categories
main_tabs = st.tabs(["Visibility & Trends", "Competitor Insights", "Brand Health", "Perception Analysis"])

# Visibility & Trends Tab
with main_tabs[0]:
    st.header("Visibility & Trends")
    st.write(
        """
        Analyze brand visibility and trends, including regional performance and emerging topics. This section
        provides insights into how well brands are represented across different platforms and regions.
        """
    )
    sub_tabs = st.tabs(["Brand Visibility", "Brand Trends", "Regional Trends", "Crisis Analysis"])

    # Brand Visibility
    with sub_tabs[0]:
        st.subheader("Brand Visibility")
        st.write("Understand how visible your brand is across various platforms and channels.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="visibility_brand_name")
        if st.button("Analyze Visibility", key="visibility_button"):
            if brand_name:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/visibility",
                        json={"brand_name": brand_name}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch visibility analysis.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Brand Trends
    with sub_tabs[1]:
        st.subheader("Brand Trends")
        st.write("Identify key trends and insights related to your brand over specific time periods.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="trends_brand_name")
        selected_time_period = st.selectbox(
            "Select the time period:",
            options=time_periods,
            key="trends_time_period"
        )

        if st.button("Analyze Trends", key="trends_button"):
            if brand_name:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/trends",
                        json={"brand_name": brand_name, "time_period": selected_time_period}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch trend analysis.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Regional Trends
    with sub_tabs[2]:
        st.subheader("Regional Trends")
        st.write("Analyze how your brand performs across different geographic regions.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="regional_trends_brand")
        region = st.text_input("Enter the region:", key="regional_trends_region")
        selected_time_period = st.selectbox(
            "Select the time period:",
            options=time_periods,
            key="regional_trends_time"
        )
        if st.button("Get Regional Trends", key="regional_trends_button"):
            if brand_name and region:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/regional_trends",
                        json={"brand_name": brand_name, "region": region, "time_period": selected_time_period}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch regional trends.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Crisis Analysis
    with sub_tabs[3]:
        st.subheader("Crisis Analysis")
        st.write("Analyze your brand's response to crises over time and identify risks.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="crisis_analysis_brand")
        selected_time_period = st.selectbox(
            "Select the time period:",
            options=time_periods,
            key="crisis_analysis_time"
        )
        if st.button("Analyze Crisis", key="crisis_analysis_button"):
            if brand_name:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/crisis_analysis",
                        json={"brand_name": brand_name, "time_period": selected_time_period}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch crisis analysis.")
                except Exception as e:
                    st.error(f"Error: {e}")

# Competitor Insights Tab
with main_tabs[1]:
    st.header("Competitor Insights")
    st.write(
        """
        Explore your competitive landscape and compare your brand's performance and visibility against competitors.
        """
    )
    sub_tabs = st.tabs(["Overall Ranking", "Brand Visibility Comparison", "Emerging Competitors", "Competitive Benchmarking"])
    
    # Overall Ranking 
    with sub_tabs[0]:
        st.subheader("Brand Overall Ranking")
        st.write("""This section provides a comparative analysis of multiple brands across defined topics. \
                 Rankings include performance for each topic and an overall score based on multiple topics.""")
        brands = st.multiselect("Select brands:", options=banking_brands, key="overall_ranking_brands")
        topics = st.multiselect("Select topics:", options=banking_topics, key="overall_ranking_topics")
       
        if st.button("Get Overall Ranking", key="overall_ranking_button"):
            if brands and topics:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/rankings",
                        json={"brands": brands, "topics": topics}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch overall ranking.")
                except Exception as e:
                    st.error(f"Error: {e}")
                    
    # Brand Comparison
    with sub_tabs[1]:
        st.subheader("Brand's Visability Comparison")
        st.write("Compare your brand's performance and visibility against competitors.")
        brand1 = st.selectbox("Select the first brand:", options=banking_brands, key="comparison_brand1")
        brand2 = st.selectbox(
            "Select the second brand:",
            options=[brand for brand in banking_brands if brand != brand1],
            key="comparison_brand2"
        )
        if st.button("Compare Brands", key="comparison_button"):
            if brand1 and brand2:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/comparison",
                        json={"brand1": brand1, "brand2": brand2}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch brand comparison.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Emerging Competitors
    with sub_tabs[2]:
        st.subheader("Emerging Competitors")
        st.write("Identify new competitors emerging in your industry.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="emerging_competitors_brand")
        industry = st.text_input("Enter the industry:", key="emerging_competitors_industry")
        if st.button("Get Emerging Competitors", key="emerging_competitors_button"):
            if brand_name and industry:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/emerging_competitors",
                        json={"brand_name": brand_name, "industry": industry}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch emerging competitors.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Competitive Benchmarking
    with sub_tabs[3]:
        st.subheader("Competitive Benchmarking")
        st.write("Compare your brand's metrics with multiple competitors over time.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="competitive_benchmarking_brand")
        competitors = st.multiselect(
            "Select competitors:",
            options=[brand for brand in banking_brands if brand != brand_name],
            key="competitive_benchmarking_competitors"
        )
        selected_time_period = st.selectbox(
            "Select the time period:",
            options=time_periods,
            key="competitive_benchmarking_time"
        )
        if st.button("Get Competitive Benchmarking", key="competitive_benchmarking_button"):
            if brand_name and competitors:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/competitive_benchmarking",
                        json={"brand_name": brand_name, "competitors": competitors, "time_period": selected_time_period}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch competitive benchmarking.")
                except Exception as e:
                    st.error(f"Error: {e}")

# Brand Health Tab
with main_tabs[2]:
    st.header("Brand Health")
    st.write(
        """
        Analyze the overall health of your brand. This section provides insights into your brand's health score
        and audience segmentation, helping you assess its performance and identify opportunities for improvement.
        """
    )
    sub_tabs = st.tabs(["Brand Health Score", "Audience Segmentation"])

    # Brand Health Score Subtab
    with sub_tabs[0]:
        st.subheader("Brand Health Score")
        st.write(
            """
            The Brand Health Score evaluates the overall performance of your brand using various metrics.
            It provides a single metric to help you understand your brand's current standing.
            """
        )
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="health_score_brand_name")

        if st.button("Analyze Brand Health Score", key="health_score_button"):
            if brand_name:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/health_score",
                        json={"brand_name": brand_name}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch brand health score.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Audience Segmentation Subtab
    with sub_tabs[1]:
        st.subheader("Audience Segmentation")
        st.write(
            """
            Understand your brand's audience by segmenting it based on various parameters, 
            providing deeper insights into your consumer base.
            """
        )
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="audience_segmentation_brand")
        time_period = st.selectbox("Select the time period:", options=time_periods, key="audience_segmentation_time")

        if st.button("Analyze Audience Segmentation", key="audience_segmentation_button"):
            if brand_name and time_period:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/audience_segmentation",
                        json={"brand_name": brand_name, "time_period": time_period}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to fetch audience segmentation.")
                except Exception as e:
                    st.error(f"Error: {e}")


# GPT Analysis Tab
with main_tabs[3]:
    st.header("GPT/Self Perception Analysis")
    st.write(
        """
        Analyze how GPT perceives your brand and compare its perception with your brand's self-representation. 
        Also, rank brands based on their self-representation across topics.
        """
    )
    sub_tabs = st.tabs(["Self Representation", "GPT Perception", "Self vs GPT Comparison", "Self Representation Ranking"])

    # Self Representation
    with sub_tabs[0]:
        st.subheader("Self Representation")
        st.write("Analyze how a brand represents itself across various topics.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="self_representation_brand")
        topics = st.multiselect(
            "Select topics:",
            options=banking_topics,
            key="self_representation_topics"
        )
        if st.button("Analyze Self Representation", key="self_representation_button"):
            if brand_name and topics:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/self_representation",
                        json={"brand_name": brand_name, "topics": topics}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to analyze self-representation.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # GPT Perception
    with sub_tabs[1]:
        st.subheader("GPT Perception")
        st.write("Analyze GPT's perception of your brand across various topics.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="gpt_perception_brand")
        topics = st.multiselect(
            "Select topics:",
            options=banking_topics,
            key="gpt_perception_topics"
        )
        if st.button("Analyze GPT Perception", key="gpt_perception_button"):
            if brand_name and topics:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/gpt_perception",
                        json={"brand_name": brand_name, "topics": topics}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to analyze GPT perception.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Self vs GPT Comparison
    with sub_tabs[2]:
        st.subheader("Self vs GPT Comparison")
        st.write("Compare your brand's self-representation with GPT's perception.")
        brand_name = st.selectbox("Select the brand:", options=banking_brands, key="self_vs_gpt_brand_name")
        topics = st.multiselect(
            "Select topics:",
            options=banking_topics,
            key="self_vs_gpt_topics"
        )
        if st.button("Compare Self vs GPT", key="self_vs_gpt_button"):
            if brand_name and topics:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/self_vs_gpt",
                        json={"brand_name": brand_name, "topics": topics}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to compare self vs GPT perception.")
                except Exception as e:
                    st.error(f"Error: {e}")

    # Self Representation Ranking
    with sub_tabs[3]:
        st.subheader("Self Representation Ranking")
        st.write("Rank brands based on their self-representation across topics.")
        brands = st.multiselect("Select brands:", options=banking_brands, key="self_representation_ranking_brands")
        topics = st.multiselect("Select topics:", options=banking_topics, key="self_representation_ranking_topics")
        if st.button("Rank Brands", key="self_representation_ranking_button"):
            if brands and topics:
                try:
                    response = requests.post(
                        f"{BACKEND_URL}/brand/self_representation_ranking",
                        json={"brands": brands, "topics": topics}
                    )
                    if response.status_code == 200:
                        st.json(response.json())
                    else:
                        st.error("Failed to rank brands by self-representation.")
                except Exception as e:
                    st.error(f"Error: {e}")
