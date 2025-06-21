from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(30), unique = True, nullable = False)
    email = db.Column(db.String(50), unique = True, nullable = False)
    password = db.Column(db.String(20), nullable = False)
class Task(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(150), nullable = False)
    description = db.Column(db.String(500), nullable = True)
    status = db.Column(db.String(256), nullable = False, default = 'new')
    created_at = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, nullable = True, default = db.func.current_timestamp(), onupdate = db.func.current_timestamp())
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    session_token = db.Column(db.String(100), unique = True, nullable = False)
    created_at = db.Column(db.DateTime, nullable = False, default = db.func.current_timestamp())