from flask import Flask, request, render_template, redirect
# from server.db.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Routes Here ==

# Login route - get users
@app.route('/users', methods=['GET'])
def display_users():
    # connection = get_flask_database_connection(app)
    return render_template('users.html', Users=Users)


# Listings route - return a list of Animals.
@app.route('/listings', methods=['GET'])
def display_listings():
    # connection = get_flask_database_connection(app)
    return render_template('listings.html')


# Test JSON route
@app.route('/profile')
def my_profile():
    response_body = {
        "name": "Nagato",
        "about" :"Hello! I'm a full stack developer that loves python and javascript"
    }

    return response_body

# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
     app.run(debug=True)