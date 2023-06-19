from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

load_dotenv()
# Create flask application
app = Flask(__name__)

# Connecting database to the server
db_uri = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
db = SQLAlchemy()

if __name__ == '__main__':
    # Import the blueprint inside the conditional statement
    from api.routes import api

    # Register the blueprint
    app.register_blueprint(api)

    # Check if the database connection is successful
    with app.app_context():
        db.init_app(app)
        db.create_all()
        print("Connected to the database successfully!")

    app.run(debug=True)