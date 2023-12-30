import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_wtf.csrf import CSRFProtect

#  define all the tools that has been used

db = SQLAlchemy()
csrf = CSRFProtect()
bootstrap = Bootstrap()
login_manager = LoginManager()
login_manager.login_view='authentication.do_login'
login_manager.session_protection = 'strong'
bcrypt = Bcrypt()

# create init app for dev, test or prod
def create_app(config_type):  # dev, test, or prod

    app = Flask(__name__)
    configuration = os.path.join(os.getcwd(), 'config', config_type + '.py')

    app.config.from_pyfile(configuration)

    db.init_app(app) # bind database to flask app
    bootstrap.init_app(app) # initalize bootstarp
    login_manager.init_app(app) # initalize login session
    bcrypt.init_app(app) # convert password into hash


# import app and register blueprint

    from app.BookAccounts import main
    app.register_blueprint(main)

    from app.auth import authentication
    app.register_blueprint(authentication)



    return app