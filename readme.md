# Installation

## Repo creation
Clone this repo
- cd into animal-adoption

## Frontend setup
Notes taken from the video - https://www.youtube.com/watch?v=ctQMqqEo4G8&t=629s

### Follow the on-screen instructions

cd frontend
npm install
npm run dev

### Frontend Dependencies
- npm install @mui/material @emotion/react @emotion/styled
- npm install react-router-dom
- npm install prop-types 


## Backend setup
This will live in a folder called 'server' just under the root.

cd server

### Create virtual environment

python -m venv adoption-venv
source adoption-venv/bin/activate

### Install dependencies 

pip install -r requirements.txt

The /frontend/.env file contains a link to the server which will provide the underlying API services. You'll need to repoint this to your flask server.

### New environment variable
cd /server/ directory
- ensure your python venv is activated
touch .env
- ensure that the .env file is in your gitignore file
- Paste the following line into your .env file (change the relevant fields!!)

DATABASE_CONNECT = "postgresql://reza@localhost:5432/adoption"
DATABASE_NAME = "adoption"
DATABASE_HOST = "localhost"
PHOTO_UPLOAD_LOCATION = "static/photo_uploads/"


# How to seed as a one-off task

ONE OFF INSTRUCTIONS to create the Postgres database.
cd /server/db
- activate your venv environment!
- type in:
 createdb adoption # to create a new postgres database

- run this file : 
python seed.py

- run this file : 
python print_seed.py

# Run the application

## Run the server application
cd server
python -m flask run --port 8000

## Run the client application
cd frontend
npm run dev


