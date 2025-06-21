from flask import Flask, Blueprint
from flask_sqlalchemy import SQLAlchemy
from app import routes as routes

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'key'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    db.init_app(app)
    from app.routes.tasks import tasks_bp
    from app.routes.auth import auth_bp
    app.register_blueprint(tasks_bp)
    app.register_blueprint(auth_bp)

    return app