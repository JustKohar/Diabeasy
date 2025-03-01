from flask import Flask, render_template

# Create a Flask app
app = Flask(__name__)

# Define a route for the home page
@app.route("/")
def home():
    return "Welcome to My Basic Website!"

# Define a route for an about page
@app.route("/about")
def about():
    return "This is the About page. Learn more about us here!"

# Define a route for a user profile page
@app.route("/user/<username>")
def user_profile(username):
    return f"Hello, {username}! Welcome to your profile."

# Run the app
if __name__ == "__main__":
    app.run(debug=True)