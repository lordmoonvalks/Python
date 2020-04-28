import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flaskblog.config import Config
from cryptography.fernet import Fernet


# key = Fernet.generate_key()
key = b'1TFTxlyXXO8NT7Gfr8qH5DSdW4auWbvC5ggE2lieYJc='
f = Fernet(key)

db = SQLAlchemy()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login' #in users blueprint
login_manager.login_message_category = 'info'  #bootstrap blue highilft 

mail = Mail()

#initialising ethe app
def create_app(config_class=Config):
	app = Flask(__name__)
	app.config.from_object(Config)

	db.init_app(app)
	bcrypt.init_app(app)
	login_manager.init_app(app)
	mail.init_app(app)
#importing all routes 
	from flaskblog.users.routes import users
	from flaskblog.posts.routes import posts
	from flaskblog.base.routes import base
	app.register_blueprint(users)
	app.register_blueprint(posts)
	app.register_blueprint(base)
	

	return app
