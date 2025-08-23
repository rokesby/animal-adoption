import time
import json
import uuid
from sqlalchemy import select
from lib.models import User
from lib.database_connection import db
from helpers.helpers import generate_pin
from lib.services.auth import  generate_token, decode_token, validate_token


def test_valid_login_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with valid credentials, 
    a 200 response should be returned"""
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 200
    
def test_incorrect_password_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect password, 
    a 401 response should be returned"""
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_email_response( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a 401 response should be returned"""
    response = client.post('/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 401
    
def test_incorrect_password_error_message( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
    
def test_incorrect_email_error_message( app_ctx,client, db_connection, test_user):
    """When a user logs in with an incorrect email, 
    a generic error message should be returned 
    'Email or password is incorrect'
    """
    response = client.post('/token', json={"email": "invalid_email@example.com", "password": "V@lidp4ss"})
    assert response.json['error'] == 'Email or password is incorrect'
    
def test_valid_login_returns_token(app_ctx, client, db_connection, test_user):
    """When a user logs in with valid credentials, a token should be returned"""
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert 'token' in response.json

def test_invalid_login_doesnt_return_token(app_ctx, client, db_connection, test_user):
    "when a user attempts login with invalid credentials, there shouldn't be a token in the response"
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "inV@lidp4ss"})
    assert 'token' not in response.json
    assert response.status_code == 401
    
def test_nonexistant_user_doesnt_return_token(app_ctx, client, db_connection, test_user):
    "when a non-existant user attempts login, there shouldn't be a token in the response"
    response = client.post('/token', json={"email": "idontexist@example.com", "password": "inV@lidp4ss"})
    assert 'token' not in response.json
    assert response.status_code == 401
    
def test_valid_login_returns_token(app_ctx, client, db_connection, test_user):
    """When a user logs in with valid credentials, a token should be returned"""
    response = client.post('/token', json={"email": "Unique_test1@example.com", "password": "V@lidp4ss"})
    assert 'token' in response.json
    
def test_protected_route_with_valid_token(client, db_connection, test_user):
    """Test accessing a protected route with a valid token"""
    response = client.post('/token', json={
        'email':test_user.email,
        'password':'V@lidp4ss'
    })
    
    token = response.json['token']

    response = client.get('/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    
    assert response.status_code == 200

def test_protected_route_without_token(client, db_connection):
    """Test accessing a protected route without a token"""
    response = client.get('/protected')
    assert response.status_code == 401
    assert response.json['message'] == 'Token is missing!'

def test_protected_route_with_invalid_token(client):
    invalid_token = 'ezJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJpc3MiOiJwYXdzZm9yYWNhdXNlIiwic3ViIjoiVW5pcXVlX3Rlc3QxQGV4YW1wbGUuY29tIiwiaWF0IjoxNzQzNjAyMzA3LCJleHAiOjE3NDM2MDU5MDcsImlkIjoxLCJzaGVsdGVyX2lkIjoxfQ.Misuk7gFhRWIXIC7pZRfgm9oKczFXBO2kkkkkKeYZ1_OM8FylPFvVqMk1dou_Z6V_h7LsRtBnmscxMeStAVhBUqDfUQOJkDDmqTXODRGgm-Xc7NUQM4LLQ5QQJMKsMUVVvpxV6_XkjN5R6BzhKp3KGew9eK1tQAIwHP_09hRD9y6WEqer2R5VJtUpPb9wMY9WcHg30mWIOqbTXHhjsv-ay572-LRz2mHgmWC5EsrfpcaWxiJQmYpWYiQCTcKD0wuPvYh53f-JOY1fIoXkW7YCQ'
    """Test accessing a protected route with an invalid token"""
    response = client.get('/protected', headers={
        'Authorization': f'Bearer {invalid_token}'
    })
    assert response.status_code == 401

def test_token_can_be_decoded_with_public_key(app_ctx, client, db_connection, test_user):
    """Test that a token can be decoded with the public key"""
    response = client.post('/token', json={
        'email': test_user.email,
        'password':'V@lidp4ss'
    })
    token = response.json['token']
    
    from lib.services.auth import decode_token
    decoded = decode_token(token)
    
    # Assert the token was decoded successfully
    assert decoded is not None
    assert decoded.claims.get('sub') == test_user.id
   
    
def test_token_is_access_token(app_ctx, client, db_connection, test_user):
    """Test that a token can be decoded with the public key"""
    response = client.post('/token', json={
        'email': test_user.email,
        'password':'V@lidp4ss'
    })
    token = response.json['token']
    
    from lib.services.auth import decode_token
    decoded = decode_token(token)
    print(f"token_type: {decoded.claims.get('token_type')}")
    # Assert the token was decoded successfully
    assert decoded is not None
    assert decoded.claims.get('token_type') == 'access'
        

def test_valid_access_token_result_is_true(app_ctx,client, db_connection, test_user, mocker):
    """
    validate_token should return True for a valid access token
    """
    
    token = generate_token(test_user.id)
    decoded = decode_token(token)
    claims = decoded.claims
    result = validate_token(claims)
    assert result == None

def test_expired_token_is_rejected(app_ctx, client, db_connection, test_user, mocker):  
    mocker.patch('lib.services.auth.time.time', return_value=1743521149)
    token_response = client.post('/token', json={
        'email': test_user.email,
        'password': 'V@lidp4ss'
    })
    token = token_response.json['token']
    print(f"token = {token}")
    mocker.patch('lib.services.auth.time.time', return_value=1743523049)
    print(f" the time now is: {time.time()}")
    
    response = client.get('/protected', headers={
        'Authorization': f'Bearer {token}'
    })
    print(response.json['message'] )
    
    assert response.status_code == 401
    assert response.json['message'] == 'expired_token: The token is expired'
    
def test_logout_removes_token(app_ctx, client, db_connection, test_user, mocker):  
    
    response = client.post('/logout')
    
    cookie_header = response.headers.get('Set-Cookie')
    print(cookie_header)
    assert response.status_code == 200
    assert 'Set-Cookie' in response.headers
    assert 'refresh_token=' in cookie_header
    assert 'Max-Age=0' in cookie_header or 'Expires=' in cookie_header
    assert response.json['message'] == 'logged out successfully'
    
def test_verification_token_invalid_for_protected_route(app_ctx, mocker, client):
    
    mocker.patch('lib.services.auth.time.time', return_value=1755173415)
    
    mock_token = mocker.Mock()
    mock_token.claims = {
        'iss': 'pawsforacause', 
        'sub': 20, 
        'iat': 1755173315, 
        'exp': 1755174115, 
        'token_type': 'verification', 
        'email': 'mock.user@example.com'
        } 
    
    mocker.patch('lib.services.auth.decode_token', return_value=mock_token)
    
    response = client.get('/protected', headers={
        'Authorization': f'Bearer {mock_token}'
    })
    
    response_data = response.get_json()
    print(response_data)
    assert response_data['message'] == "Invalid token type"

def test_valid_pin_verifies_user(app_ctx, client, mocker, verification_repo):
    """
    GIVEN a valid pin is entered
    POST /verify/token123
    should update 'verified' to true
    """
    # take pin input from user
    # validate pin matches bcrypt hash
    # flask_bcrypt.check_password_hash(hashed_pin, plain_pin)
    # the token will be passed in the post request
    verification_id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    
    mocker.patch('lib.services.auth.time.time', return_value=1755173315)
    
    verification_token = generate_token(verification_id, token_type='verification')
    
    mocker.patch('lib.services.auth.time.time', return_value=1755173615)
    

    response = client.post('/verify',json={
        'pin': '123456',
        'token': verification_token
    })
    
    assert response.status_code == 200
    
def test_unverified_user_cannot_log_in(client, verification_repo):
    """
    GIVEN a user attempts to log in
    IF 'verified' is False
    an access token shouldn't be issued
    """
    response = client.post('/token', json={"email": "unverified.user@example.com", "password": "V@lidp4ss"})
    assert response.status_code == 403


def test_reverify_with_valid_user_returns_201(client, mocker, verification_repo):
    
    mock_data = {
    "email": "unverified.user@example.com",
    }
    
    mock_send_verification_email = mocker.patch('routes.auth_routes.send_verification_email', return_value=202)
    
    response = client.post('/reverify', json=mock_data)
    assert response.status_code == 200
    mock_send_verification_email.assert_called_once()
    
def test_reverify_with_valid_user_returns_404(client, mocker, verification_repo):
    
    mock_data = {
    "email": "doesnt.exist@example.com",
    }
    
    response = client.post('/reverify', json=mock_data)
    assert response.status_code == 404
    
def test_reverify_verified_user_returns_500(client, mocker, verification_repo):
    
    mock_data = {
    "email": "verified.user@example.com",
    }
    
    response = client.post('/reverify', json=mock_data)
    assert response.status_code == 500
    