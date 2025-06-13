
from dotenv import load_dotenv
import os
from functools import wraps
from flask import jsonify, request, current_app
import time
from joserfc.jwk import RSAKey
from joserfc import jwt, errors
from joserfc.jwt import JWTClaimsRegistry
from flask import g

load_dotenv()

# secret = os.getenv('SECRET_KEY')
# current_app.config['SECRET_KEY']

class TokenClaimsRegistry(JWTClaimsRegistry):
    def __init__(self, now = None, leeway = 0, **kwargs):
        super().__init__(now, leeway, **kwargs)
        
    def validate(self, claims):
        if claims.get('iss') != 'pawsforacause':
            raise ValueError("Issuer isn't valid!")
        return super().validate(claims)


def generate_token(user_id, additional_claims=None, token_type='access'):
    private_jwk = current_app.config['JWT_PRIVATE_KEY']
   
    if token_type == 'access':
        expiry = current_app.config['ACCESS_TOKEN_EXPIRY']
    else:
        expiry = current_app.config['REFRESH_TOKEN_EXPIRY']
        
    current_time = int(time.time())
    expiry_time = expiry + int(time.time())
    
    header = {'alg': 'RS256'}
    
    claims = {
        "iss": "pawsforacause",
        "sub": int(user_id),
        "iat": current_time,
        "exp": expiry_time,
        "token_type": token_type
    }
    
    if additional_claims:
        claims.update(additional_claims)
    
    print(f"Generating token with claims: {claims}") 
    token = jwt.encode(header, claims, private_jwk)
    return token

def validate_token(claims):
    token_type = claims.get('token_type')
    
    if token_type == 'access':
        token_leeway = current_app.config['ACCESS_TOKEN_EXPIRY']
    elif token_type == 'refresh':
        token_leeway = current_app.config['REFRESH_TOKEN_EXPIRY']
    else:
        raise ValueError("token_type isn't valid")
    
    token_claims_registry = TokenClaimsRegistry(leeway=token_leeway)
    
    print(f"About to validate {token_type} claims...")

    token_claims_registry.validate(claims)
    token_claims_registry.validate_iat(claims.get('iat'))
    token_claims_registry.validate_exp(claims.get('exp'))

    
def update_request_data(decoded_token):
    # claims = decoded_token.claims
    # if decoded_token.claims.get('id') is None:
    #     print(f"Token missing user.id")
    #     return jsonify({"message": "Token missing user.id"}), 401
    # else:
    #     user_id = decoded_token.claims.get('id')
    #     print(f"user_id = {user_id}")
    #     g.user_id = user_id
    
    # if decoded_token.claims.get('shelter_id'):
    #     shelter_id = decoded_token.claims.get('shelter_id')
    #     g.shelter_id = shelter_id
    pass

def decode_token(token):
    public_jwk = current_app.config['JWT_PUBLIC_KEY']
    
    try:
        decoded_token = jwt.decode(token, public_jwk, algorithms=["RS256"])
        return decoded_token  
    
    except Exception as e:
        print(f"Token decoding failed: {e}")
    
# Function is passed as an argument to token_checker(f)
def token_checker(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        # my ACCESS token I send in the header
        # my REFRESH token is sent in the cookie
        auth_header = request.headers.get('Authorization') 
        
        if not auth_header or not auth_header.startswith('Bearer '):
            return jsonify({"message": "Token is missing!"}), 401
        else:
            token = auth_header.split(" ")[1]
            
        try:
            decoded_token = decode_token(token)
            print(f"decoded token: {decoded_token}")
            if not decoded_token or decoded_token == None:
                raise Exception("Token decoding failed")
            
            token_type = decoded_token.claims.get('token_type')
            print(f"decoded token type: {token_type}")
            if token_type != 'access':
                raise Exception("Invalid token type")
            
            print(f"token claims: {decoded_token.claims}")
            if validate_token(decoded_token.claims) == False:
                raise Exception("Token claims aren't valid")
            
        except Exception as e:
            print(f"Error processing token claims: {str(e)}")
            return jsonify({"message":  f"{str(e)}"}), 401

        return f(*args, **kwargs)

    return decorated_function


# // Gather the values
# secret = readEnvironmentVariable("CSRF_SECRET") // HMAC secret key
# sessionID = session.sessionID // Current authenticated user session
# randomValue = cryptographic.randomValue() // Cryptographic random value

# // Create the CSRF Token
# message = sessionID.length + "!" + sessionID + "!" + randomValue.length + "!" + randomValue // HMAC message payload
# hmac = hmac("SHA256", secret, message) // Generate the HMAC hash
# csrfToken = hmac + "." + randomValue // Add the `randomValue` to the HMAC hash to create the final CSRF token. Avoid using the `message` because it contains the sessionID in plain text, which the server already stores separately.

# // Store the CSRF Token in a cookie
# response.setCookie("csrf_token=" + csrfToken + "; Secure") // Set Cookie without HttpOnly flag``

