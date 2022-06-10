# makes the parent folder as a python package
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    
    # Encrypt the cookies and session data
    app.config['SECRET_KEY'] = 'this is my flask app'
    # Giving the path to store the db
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    # Telling db that our app is this
    db.init_app(app)
    
    # Register the blueprint
    from .views import views
    from .auth import auth
    
    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    
    # To make sure these below classes run 
    from .models import User, EncryptedData
    
    create_database(app)

    login_manager = LoginManager()
    # redirect the user if the user is not logged in
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)
    
    # tells flask that how the server is loading the user. By default looks the primary key which is the 'id'
    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    return app

# Function to initiate the DB creation if not created
def create_database(app):
    if not path.exists('website/'+DB_NAME):
        db.create_all(app=app)
        print('Created Database!!')
        
        
        
        