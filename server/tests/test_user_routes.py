"""
GIVEN a valid first name, last name, email and password
POST /sign-up should generate a pin
"""
import uuid
import pytest
from lib.models.user import User
from helpers import helpers

def test_signup_route_generate_pin_called(client, mocker, db_connection):
    
    user_data = {
        "first_name": "mock",
        "last_name": "user",
        "email": "mock.user@example.com",
        "password": "V@LidP4ss"
    }
    
    mock_generate_pin = mocker.patch('routes.user_routes.generate_pin', return_value=('123456', 'thisishashed'))
    
    mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=user_data)
    assert response.status_code == 201
    mock_generate_pin.assert_called_once()
    
def test_signup_route_create_user_called(client, mocker, verification_repo):
    
    mock_data = {
        "first_name": "mock",
        "last_name": "user",
        "email": "mock.user@example.com",
        "password": "V@LidP4ss"
    }
    
    mocker.patch('routes.user_routes.shelter_repository.get_shelter_id_by_domain', return_value=None)
    
    mock_user = mocker.Mock(spec=User)
    mock_user.id = 20
    mock_user.first_name = "mock"
    mock_user.last_name = "user"

    mock_create_user = mocker.patch('routes.user_routes.user_repository.create_user', return_value=mock_user)

    
    mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=mock_data)
    assert response.status_code == 201
    mock_create_user.assert_called_once()
    
def test_signup_route_get_shelter_id_by_domain_called(client, mocker, db_connection):
    
    
    mock_data = {
        "first_name": "mock",
        "last_name": "user",
        "email": "mock.user@example.com",
        "password": "V@LidP4ss"
    }
    
    mock_get_shelter_id_by_domain = mocker.patch('routes.user_routes.shelter_repository.get_shelter_id_by_domain', return_value=None)
    
    mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=mock_data)
    assert response.status_code == 201
    mock_get_shelter_id_by_domain.assert_called_once()
    
def test_generate_verification_token_is_called(client, mocker, verification_repo):
    
    mock_data = {
        "first_name": "mock",
        "last_name": "user",
        "email": "mock.user@example.com",
        "password": "V@LidP4ss"
    }
    
    mock_token = mocker.Mock()
    
    mock_generate_token = mocker.patch('routes.user_routes.generate_token', return_value=mock_token)
    
    mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=mock_data)
    assert response.status_code == 201
    mock_generate_token.assert_called_once()
    
def test_send_verification_email_is_called(client, mocker, verification_repo):
    
    mock_data = {
        "first_name": "mock",
        "last_name": "user",
        "email": "mock.user@example.com",
        "password": "V@LidP4ss"
    }
    
    
    mock_send_verification_email = mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=mock_data)
    assert response.status_code == 201
    mock_send_verification_email.assert_called_once()

def test_signup_add_verification_is_called(client, mocker, db_connection):
    
    mock_data = {
    "first_name": "mock",
    "last_name": "user",
    "email": "mock.user@example.com",
    "password": "V@LidP4ss"
}
    verification_entry = mocker.Mock()
    verification_entry.id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    
    mock_add_verification = mocker.patch('routes.user_routes.verification_repository.add_verification', return_value=verification_entry)
    
    mocker.patch('routes.user_routes.send_verification_email', return_value=202)
    
    response = client.post('/sign-up', json=mock_data)
    assert response.status_code == 201
    mock_add_verification.assert_called_once()
    
    