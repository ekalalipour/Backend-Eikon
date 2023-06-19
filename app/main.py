from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Create flask application
app = Flask(__name__)

# Connecting database to the server
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://utqrmtxr:w0XHRA1e0K69NeGUlvcxTg3lVru4FsHS@mahmud.db.elephantsql.com/utqrmtxr'
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