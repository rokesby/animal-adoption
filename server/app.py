from flask import Flask, request, render_template, redirect
# from lib.database_connection import get_flask_database_connection

# Create a new Flask app
app = Flask(__name__)

# == Your Routes Here ==


# == Example Code Below ==

# GET /emoji
# Returns a smiley face in HTML
# Try it:
#   ; open http://localhost:5001/emoji
# @app.route('/emoji', methods=['GET'])
# def get_emoji():
    # We use `render_template` to send the user the file `emoji.html`
    # But first, it gets processed to look for placeholders like {{ emoji }}
    # These placeholders are replaced with the values we pass in as arguments
    # return render_template('emoji.html', emoji=':)')



# Login route - capture
# @app.route('/login', methods=['GET'])
# def display_login_page():
#     return render_template('login.html')


# These lines start the server if you run this file directly
# They also start the server configured to use the test database
# if started in test mode.
if __name__ == '__main__':
     app.run(debug=True)