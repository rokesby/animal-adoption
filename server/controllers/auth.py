from authlib.jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()

# Encoding a JWT
header = {'alg': 'HS256'}
secret = os.getenv('SECRET_KEY')


def generate_token(user_id):
    token = jwt.encode(
        {
            'alg': 'HS256'}, 
        {
            "user_id": user_id
        }, 
        secret
        )
    return token


def decode_token(token):
  return jwt.decode(token, secret)



# const JWT = require("jsonwebtoken");

# // Middleware function to check for valid tokens
# const tokenChecker = (req, res, next) => {
#   let token;
#   const authHeader = req.get("Authorization");

#   if (authHeader) {
#     token = authHeader.slice(7);
#   }

#   JWT.verify(token, process.env.JWT_SECRET, (err, payload) => {
#     if (err) {
#       console.log(err);
#       res.status(401).json({ message: "auth error" });
#     } else {
#       // Add the user_id from the payload to the req object.
#       req.user_id = payload.user_id;
#       next();
#     }
#   });
# };

# module.exports = tokenChecker;