# Installation

## Repo creation
Clone this repo
- cd into animal-adoption

# Frontend setup
Notes taken from the video - https://www.youtube.com/watch?v=ctQMqqEo4G8&t=629s

## Follow the on-screen instructions

- cd frontend
- npm install
- npm run dev

# Backend setup
This will live in a folder called 'server' just under the root.

cd server

## Create virtual environment
- python -m venv adoption
- source adoption/bin/activate

## Install dependencies 
- pip install flask
- pip install pymongo
- pip install psycopg2
- pip install SQLAlchemy
- pip install -U Flask-SQLAlchemy
- pip install python-dotenv


## Frontend Dependencies
- npm install @mui/material @emotion/react @emotion/styled
- npm install react-router-dom 

# How to seed.... (one-off)
ONE OFF INSTRUCTIONS to create the Postgres database.
- go to /server/db
- activate your venv environment!
- type in createdb adoption # to create a new postgres database
- run this file : python seed.py
- run this file : python print_seed.py

# New environment variable
- go to /server/ directory
- ensure your python venv is activated
- touch .env
- ensure that the .env file is in your gitignore file
- Paste the following line into your .env file (change the relevant fields!!)

DATABASE_CONNECT = "postgresql://reza@localhost:5432/adoption"
DATABASE_NAME = "adoption"
DATABASE_HOST = "localhost"
