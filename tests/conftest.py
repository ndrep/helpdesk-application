import os
import tempfile
import pytest
from backend.server import create_app

@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({
        'TESTING':True,
        'SQLALCHEMY_DATABASE_URI': ''.join(['sqlite:////', db_path]),
    })
    with app.app_context():
        from backend.server.json_loader import load_db
        load_db('backend/server/data.json')

    yield app
    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture
def client(app):
    _client = app.test_client()
    return _client