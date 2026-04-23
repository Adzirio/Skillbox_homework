import pytest
from app import create_app

@pytest.fixture(scope="session")
def app():
    app = create_app()
    app.config.update(TESTING=True, SQLALCHEMY_DATABASE_URL="sqlite:///test.db")
    return app

@pytest.fixture()
def client(app):
    return app.test_client()