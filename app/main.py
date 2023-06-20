from flask import Flask
from dotenv import load_dotenv
import os
from flask_cors import CORS
from api.routes import api, db


load_dotenv()

# Create flask application
app = Flask(__name__)
CORS(app)

# Connecting database to the server
db_uri = os.environ.get('DATABASE_URI')
app.config['SQLALCHEMY_DATABASE_URI'] = db_uri
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db.init_app(app)

# Import the blueprint
from api.routes import api

# Register the blueprint
app.register_blueprint(api)

if __name__ == '__main__':
    # Check if the database connection is successful
    with app.app_context():
        db.create_all()
        print("Connected to the database successfully!")
        with app.app_context():
          app.run(debug=True, host='0.0.0.0', port=8080)
    

