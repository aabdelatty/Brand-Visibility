import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))


from fastapi.testclient import TestClient
from app import app

# Initialize the TestClient
client = TestClient(app)

def test_brand_visibility_success():
    payload = {"brand_name": "Nike"}
    response = client.post("/brand/visibility", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "visibility_score" in data
    assert "key_sentiments" in data
    assert "top_topics" in data
    assert "top_regions" in data

def test_brand_visibility_invalid_payload():
    payload = {}  # Missing 'brand_name'
    response = client.post("/brand/visibility", json=payload)
    assert response.status_code == 422  # FastAPI validation error

def test_brand_comparison_success():
    payload = {"brand1": "Nike", "brand2": "Adidas"}
    response = client.post("/brand/comparison", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "brand1_visibility" in data
    assert "brand2_visibility" in data
    assert "differentiators" in data

def test_brand_comparison_invalid_payload():
    payload = {"brand1": "Nike"}  # Missing 'brand2'
    response = client.post("/brand/comparison", json=payload)
    assert response.status_code == 422  # FastAPI validation error

def test_trend_analysis_success():
    payload = {"brand_name": "Apple", "time_period": "2023-11"}
    response = client.post("/brand/trends", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "trending_topics" in data
    assert "emerging_regions" in data

def test_trend_analysis_invalid_payload():
    payload = {"brand_name": "Apple"}  # Missing 'time_period'
    response = client.post("/brand/trends", json=payload)
    assert response.status_code == 422  # FastAPI validation error

def test_emerging_competitors_success():
    payload = {"brand_name": "Tesla", "industry": "Automotive"}
    response = client.post("/brand/emerging_competitors", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "competitors" in data

def test_emerging_competitors_invalid_payload():
    payload = {"brand_name": "Tesla"}  # Missing 'industry'
    response = client.post("/brand/emerging_competitors", json=payload)
    assert response.status_code == 422  # FastAPI validation error

# Add similar tests for all other endpoints...

