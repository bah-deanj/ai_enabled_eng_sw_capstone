import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy.pool import StaticPool
from app.main import Base  # Adjust the import based on actual app structure
from app.main import get_db  # Adjust the import based on actual app structure
from fastapi.testclient import TestClient
from app.main import app  # Adjust the import based on actual app structure

# Create a new SQLAlchemy engine for an in-memory SQLite database
SQLALCHEMY_DATABASE_URL = "sqlite://"

# Fixture to create and destroy the database schema
@pytest.fixture(scope="function")
def db_engine():
    engine = create_engine(
        'sqlite:///:memory:', 
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,  # Use StaticPool to ensure connection reuse
        echo=False
    )
    Base.metadata.create_all(engine)
    yield engine
    Base.metadata.drop_all(engine)


@pytest.fixture(scope='function')
def db_session(test_engine):
    # Create a session using the shared test engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)
    session = SessionLocal()
    yield session
    session.close()


@pytest.fixture(scope='function')
def client(test_engine):
    # Create a SessionLocal bound to the same test engine
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=test_engine)

    def _get_test_db():
        db = SessionLocal()
        try:
            # Ensure tables exist in this session's connection
            Base.metadata.create_all(db.get_bind())
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = _get_test_db

    client = TestClient(app)
    try:
        yield client
    finally:
        app.dependency_overrides.clear()