import pytest, sys, random, py, os
from server import app
from server.db import db
from server.db.database_connection import db_session

@pytest.fixture
def app():
    app = create_app({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()


@pytest.fixture 
def client(app):
    app.config['TESTING'] = True # This gets us better errors
    return app.test_client()
