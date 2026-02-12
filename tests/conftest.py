"""Pytest configuration and fixtures"""
import pytest
from fastapi.testclient import TestClient
from src.api.main import app
import os

# Set test environment variables
os.environ["GROQ_API_KEY"] = "test-key"
os.environ["TAVILY_API_KEY"] = "test-key"

@pytest.fixture
def client():
    """FastAPI test client"""
    return TestClient(app)

@pytest.fixture
def mock_env(monkeypatch):
    """Mock environment variables"""
    monkeypatch.setenv("GROQ_API_KEY", "test-key")
    monkeypatch.setenv("TAVILY_API_KEY", "test-key")
