


from flask_sqlalchemy import SQLAlchemy
from flask_bootstrap import Bootstrap
from flask_login import LoginManager
from flask import Flask
from flask_moment import Moment
from flask_whooshee import Whooshee
from flask_wtf import CSRFProtect
from flask_migrate import Migrate



db=SQLAlchemy()
bootstrap=Bootstrap()
login_manager=LoginManager()
moment=Moment()
whooshee=Whooshee()
csrf = CSRFProtect()
migrate=Migrate()


@login_manager.user_loader
def load_user(username):
    from spotify.models import Admin
    user = Admin.query.get(username)
    return user


def create_app():
    app = Flask(__name__)
    db.init_app(app)
    return app





