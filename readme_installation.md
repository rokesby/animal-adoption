# Installation

## Repo creation
Clone this repo
- cd into animal-adoption

# Frontend setup
Notes taken from the video - https://www.youtube.com/watch?v=ctQMqqEo4G8&t=629s

## Follow the on-screen instructions

cd frontend
npm install
npm run dev

# Backend setup
This will live in a folder called 'server' just under the root.

cd server
.env file - Add SECRET_KEY="SecretKeyHere"

Generate a secret key
>>> import secrets
>>> secret_key = secrets.token_hex(32)
>>> print(secret_key)

## Create virtual environment

python -m venv adoption-venv
source adoption-venv/bin/activate

## Install dependencies 

pip install -r requirements.txt


## Frontend Dependencies
- npm install @mui/material @emotion/react @emotion/styled
- npm install react-router-dom
- npm install prop-types 


# New environment variable
cd /server/ directory
- ensure your python venv is activated
touch .env
- ensure that the .env file is in your gitignore file
- Paste the following line into your .env file (change the relevant fields!!)

DATABASE_CONNECT = "postgresql://reza@localhost:5432/adoption"
DATABASE_NAME = "adoption"
DATABASE_HOST = "localhost"
PHOTO_UPLOAD_LOCATION = "static/photo_uploads/"

