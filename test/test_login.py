
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
import pytest
from fastapi.testclient import TestClient
from httpx import AsyncClient

from main import app
from db.mongo import users_collection
import bcrypt

@pytest.mark.asyncio
async def test_login_client_user():
    # Ensure user exists
    await users_collection.insert_one({
        "email": "clienttest@example.com",
        "password": bcrypt.hashpw("password123".encode(), bcrypt.gensalt()).decode(),
        "user_type": "client",
        "is_verified": True
    })

    async with AsyncClient(app=app, base_url="http://test") as ac:
        response = await ac.post("/auth/login", json={
            "email": "clienttest@example.com",
            "password": "password123"
        })
        assert response.status_code == 200
        assert "access_token" in response.json()