"""Shared fixtures; every test receives a fresh, isolated SQLite database."""
import pytest
from app import app
from db import init_db, create_task


@pytest.fixture
def client(tmp_path, monkeypatch):
    db_file = tmp_path / 'tasks.db'
    monkeypatch.setitem(app.config, 'TESTING', True)
    monkeypatch.setitem(app.config, 'DB_NAME', str(db_file))
    init_db(str(db_file))
    with app.test_client() as test_client:
        yield test_client


@pytest.fixture
def db_path(tmp_path):
    path = str(tmp_path / 'unit_tasks.db')
    init_db(path)
    return path


@pytest.fixture
def seeded_client(client):
    db_path = app.config['DB_NAME']
    create_task('Write tests', 'SQE assignment', '2026-10-21', 'pending', db_path)
    return client
