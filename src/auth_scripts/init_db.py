import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from models.user_model import db
from app import app

with app.app_context():
    db.create_all()
    print("Database initialized!")
