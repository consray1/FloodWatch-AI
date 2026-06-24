import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.main import app
from app.core.database import Base, get_db
from app.models import Role

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@pytest.fixture
def db():
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture
def client(db):
    def override_get_db():
        try:
            yield db
        finally:
            pass

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as c:
        yield c
    app.dependency_overrides.clear()


@pytest.fixture
def citizen_role(db):
    role = Role(name="citizen", description="Test role")
    db.add(role)
    db.commit()
    return role


@pytest.fixture
def admin_role(db):
    role = Role(name="admin", description="Admin role")
    db.add(role)
    db.commit()
    return role


@pytest.fixture
def test_user(db, citizen_role):
    from app.core.security import get_password_hash
    from app.models import User

    user = User(
        name="Test User",
        email="test@example.com",
        password_hash=get_password_hash("TestPass123"),
        role_id=citizen_role.id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@pytest.fixture
def auth_token(client, test_user):
    response = client.post("/api/v1/auth/login", json={
        "email": "test@example.com",
        "password": "TestPass123"
    })
    return response.json()["access_token"]