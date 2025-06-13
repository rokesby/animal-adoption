# Installation

## Repo creation
Clone this repo - Note: I have named the directory animal-adoption-app for consistency but you can name it whatever you like!
```zsh
git clone https://github.com/Matt-Wilkes/python-react-animal-adoption-app.git animal-adoption-app
cd animal-adoption-app
```

## Frontend setup
```zsh
cd frontend
npm install
```

## Backend setup
This will live in a folder called 'server' just under the root.
```zsh
cd server
```

### 1. Create virtual environment

```zsh
python -m venv animal-adoption-app-venv 
source animal-adoption-app-venv/bin/activate 
```
### 2. Install dependencies 
```zsh
pip install -r requirements.txt
```

### 3. Create a local database

In the terminal: 
```zsh
cd db
createdb animal_adoption_app
```

### Add environment variables
In a new terminal:
Generate a secret key in Python repl:
```zsh
python
import secrets
print(secrets.token_hex(32)) # copy the secret key generated here
exit()
```

```zsh
# create a .env file with your secret key in the same directory (server)
echo SECRET_KEY=\"ReplaceThisWithYourSecretKey\" >> .env
# check the .env file has been created and updated with your secret key
open .env
```
<!-- add the below to your .env file: -->
NODE_ENV="development"
DATABASE_CONNECT = "postgresql://your-user-name@localhost:5432/animal_adoption_app"
DATABASE_NAME = "animal_adoption_app"
DATABASE_HOST = "localhost"
PHOTO_UPLOAD_LOCATION = "static/photo_uploads/"

### New environment variable

The /frontend/.env file contains a link to the server which will provide the underlying API services. You'll need to repoint this to your flask server.

in the /frontend directory
```zsh
# create the .env file
echo VITE_BACKEND_URL="http://127.0.0.1:5000" >> .env
# check the .env file has been created and updated with your secret key
open .env
```

# Initialising the database
in the server/ directory run the below commands
```zsh
flask init-db
flask seed-db
```

- run this file : 
python print_seed.py

# Run the application
You'll need to run the server in one terminal and the frontend in another terminal window

## Run the server application
```zsh
cd server
python -m flask run
```

## Run the client application
```zsh
cd frontend
npm run dev
```

# Demonstration video

[Animal Adoption 1](https://youtu.be/9EJpEnw2uaQ)
[Animal Adoption 2](https://youtu.be/str5xphRq-s)