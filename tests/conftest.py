import pytest
from app import create_app, db


TEST_CONFIG = {
    "TESTING": True,
    "SQLALCHEMY_DATABASE_URI": "sqlite:///:memory:",
    "LOG_LEVEL": "DEBUG"
}


@pytest.fixture
def app():
    app = create_app(TEST_CONFIG)

    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()
