import time
import pytest
import json

from sqlalchemy import select
from lib.models import User
from lib.database_connection import db
from routes.auth import TokenClaimsRegistry, JWTClaimsRegistry, generate_token, decode_token, validate_token
from joserfc.errors import *
from flask import current_app



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
    
    from routes.auth import decode_token
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
    
    from routes.auth import decode_token
    decoded = decode_token(token)
    print(f"token_type: {decoded.claims.get('token_type')}")
    # Assert the token was decoded successfully
    assert decoded is not None
    assert decoded.claims.get('token_type') == 'access'

def test_token_claims_registry_valid_claims(app_ctx,db_connection, mocker):
    """
    TokenClaimsRegistry should validate correctly formed access token claims
    """
    token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    current_time = int(time.time())
    expiry = current_app.config['ACCESS_TOKEN_EXPIRY']
    
    valid_claims = {
        "iss": "pawsforacause",
        "sub": "test_user@example.com",
        "iat": current_time,
        "exp": current_time + expiry,
        "token_type": "access"
    }
   
    mock_super_validate = mocker.patch.object(JWTClaimsRegistry, 'validate', return_value=None)
    
    result = token_claims_registry.validate(valid_claims)
    
    assert result is None 
    mock_super_validate.assert_called_once_with(valid_claims)


# def test_token_claims_registry_invalid_token_type(app_ctx,db_connection,mocker):
#     """
#     Should raise ValueError when token type is not valid
#     """
    
#     invalid_claims = {
#         "iss": "pawsforacause", 
#         "token_type": "pretend" 
#     }
    
#     with pytest.raises(ValueError) as err:
#         token_claims_registry.validate(invalid_claims)
#     error_message = str(err.value)
#     print(error_message)
#     assert error_message == "token_type isn't valid"

    
def test_token_claims_registry_iat_not_yet_valid(app_ctx,db_connection,mocker):
    """
    Should raise InvalidTokenError when iat is in the future
    """
    token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    current_time = int(time.time())
    
    invalid_claims = {
        "iss": "pawsforacause", 
        "token_type": "access",
        "iat": current_time + 30000,
    }
    
    with pytest.raises(InvalidTokenError) as err:
        token_claims_registry.validate(invalid_claims)
    error_message = str(err.value.description)
    assert error_message == 'The token is not valid yet'
    
def test_token_claims_registry_exp_invalid(app_ctx,db_connection,mocker):
    """
    Should raise InvalidTokenError when 'exp' is in the past
    """
    
    token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    # mocker.patch('routes.auth.time.time', return_value=1743521149)
    
    invalid_claims = {
        "iss": "pawsforacause", 
        "token_type": "access",
        "exp": 1743521149,
    }
    
    with pytest.raises(ExpiredTokenError) as err:
        token_claims_registry.validate(invalid_claims)
    error_message = str(err.value)
    print(error_message)
    assert error_message == 'expired_token: The token is expired'
    
def test_token_claims_registry_iat_is_valid(app_ctx,db_connection):
    """
    Should return None when 'iat' time is in the past
    """
    
    token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    current_time = int(time.time())
    
    valid_claims = {
        "iss": "pawsforacause", 
        "token_type": "access",
        "iat": current_time,
    }
    
    response = token_claims_registry.validate_iat(valid_claims.get('iat'))
    print(response)
    assert response == None
    
def test_token_claims_registry_invalid_issuer(app_ctx,db_connection,mocker):
    """
    Should raise ValueError when issuer is not 'pawsforacause'
    """
    token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    
    invalid_claims = {
        "iss": "notpawsforacause", 
        "token_type": "access" 
    }
    
    with pytest.raises(ValueError) as err:
        token_claims_registry.validate(invalid_claims)
    error_message = str(err.value)
    print(error_message)
    assert error_message == "Issuer isn't valid!"
        

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
    mocker.patch('routes.auth.time.time', return_value=1743521149)
    token_response = client.post('/token', json={
        'email': test_user.email,
        'password': 'V@lidp4ss'
    })
    token = token_response.json['token']
    print(f"token = {token}")
    mocker.patch('routes.auth.time.time', return_value=1743523049)
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
    
