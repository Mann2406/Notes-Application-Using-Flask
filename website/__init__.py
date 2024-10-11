import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = "Mann Flask Website"
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("DATABASE_URL")
    # database_url = os.environ.get("DATABASE_URL")
    # if not database_url:
    #     raise RuntimeError("DATABASE_URL environment variable is not set.")
    #     app.config['SQLALCHEMY_DATABASE_URI'] = database_url

    # postgresql://notesapp_wy08_user:vyy1rMZQaLAQlqkBVmLeXqt2x6UZiQY1@dpg-cs13cglds78s73b31q20-a.oregon-postgres.render.com/notesapp_wy08

    db.init_app(app)

    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User, Note

    with app.app_context():
        db.create_all()

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
        
    return app

def create_database(app):
    if not path.exists('website/' + DB_NAME):
        db.create_all(app)
        print("Created Database!")