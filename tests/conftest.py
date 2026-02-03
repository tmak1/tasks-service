import pytest
import sys
import os
import jwt
import datetime
from unittest.mock import patch  # <--- STANDARD: Use Mocking

# Add parent dir to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app
from database import Base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session

TEST_DATABASE_URL = "sqlite:///:memory:"

@pytest.fixture(scope='session')
def test_engine():
    return create_engine(TEST_DATABASE_URL)

@pytest.fixture(scope='function')
def client(test_engine):
    # 1. Create tables in the isolated SQLite DB
    Base.metadata.create_all(test_engine)
    
    # 2. Create a Transactional Connection (Rolls back after test)
    connection = test_engine.connect()
    transaction = connection.begin()
    TestSession = scoped_session(sessionmaker(bind=connection))
    
    # 3. THE FIX: Patch 'Session' specifically inside 'tasks_routes'
    # This forces the API to use our SQLite session, ignoring the real DB.
    with patch('tasks_routes.Session', TestSession):
        with app.test_client() as client:
            yield client

    # 4. Teardown
    transaction.rollback()
    connection.close()
    Base.metadata.drop_all(test_engine)

@pytest.fixture
def auth_header():
    # Create a fake Admin token for testing
    token_payload = {
        'user_id': 1,
        'role': 'user',
        'exp': datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(hours=1)
    }
    token = jwt.encode(token_payload, 'secret', algorithm="HS256")
    return {'Authorization': f'Bearer {token}'}