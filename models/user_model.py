from app import app
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, UserMixin
from sqlalchemy import event
import uuid

db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    api_key = db.Column(db.String(36), unique=True, nullable=False, default=lambda: str(uuid.uuid4()))

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.is_admin}')"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Сигнал для обновления состояния объекта пользователя
@event.listens_for(User, 'after_update')
def refresh_object(mapper, connection, target):
    db.session.refresh(target)