import time
import uuid
import pytest
from lib.services.auth import TokenClaimsRegistry, JWTClaimsRegistry, decode_token, generate_token, validate_token
from flask import current_app
from joserfc.errors import *

from lib.models.user import User
from lib.models.verification import Verification

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
    # mocker.patch('lib.services.auth.time.time', return_value=1743521149)
    
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



def test_generate_verification_token(app_ctx, mocker, db_connection):
    """
    GIVEN a valid id,
    generate_verification_token should generate a jwt
    WITH a sub matching verification_id
    """
    mock_user = mocker.Mock(spec=User)
    mock_user.id = 20
    
    mock_verification = mocker.Mock(spec=Verification)
    mock_verification.id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
    
    
    mock_bcrypt = "$2a$12$WUI1ZnJ7y5qWIc/grnewbO9sekcpQbtRrV6N0awLgq25wcORN2zge"
    
    
    mocker.patch('lib.services.auth.time.time', return_value=1755173415)
    print(f" the time now is: {time.time()}")
    
    mock_expiry = 1755173415 + current_app.config['ACCESS_TOKEN_EXPIRY']
    token = generate_token(mock_verification.id, token_type='verification')
    
    result = decode_token(token).claims
    assert result['iss'] == "pawsforacause"
    assert result['sub'] == '5235c2d2-266a-4851-a48a-777ce595065e'
    assert result['token_type'] == "verification"
    assert result['iat'] == 1755173415
    assert result['exp'] == mock_expiry

def test_valid_verification_token_expiry_returns_none(app_ctx, mocker, db_connection):
    mock_token = mocker.Mock()
    mock_token.claims = {
        'iss': 'pawsforacause', 
        'sub':'5235c2d2-266a-4851-a48a-777ce595065e', 
        'iat': 1755173315, 
        'exp': 1755174115, 
        'token_type': 'verification', 
        } 
    
    mocker.patch('lib.services.auth.time.time', return_value=1755173415)
    mocker.patch('lib.services.auth.decode_token', return_value=mock_token)
    
    result = validate_token(mock_token.claims)

    assert result is None
    
# def test_verify_user_pin_is_valid(app_ctx, mocker, verification_repo):
#     """
#     GIVEN a valid pin
#     verify_user_pin should return the user
#     """
    
#     mocker.patch('lib.services.auth.time.time', return_value=1755173415)
    
#     plain_pin = '123456'
#     verification_id = uuid.UUID('5235c2d2-266a-4851-a48a-777ce595065e')
#     # call get_verification_by_id
#     # id bcrypt user pin = hashed pin
#     # return user id
#     # else return None
#     verified_user = verify_user_pin(plain_pin, verification_id)
    
#     assert verified_user == 20
    