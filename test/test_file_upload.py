import pytest
from httpx import AsyncClient, ASGITransport

import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from main import app

@pytest.mark.asyncio
async def test_client_signup():
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        response = await ac.post("/client/signup", json={
            "email": "testuser@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "verification_token" in response.json()
