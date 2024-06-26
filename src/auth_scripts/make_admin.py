import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
print(os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))
from models.user_model import db, User
from app import app

def make_admin(email, is_admin):
    with app.app_context():
        user = User.query.filter_by(email=email).first()
        if user:
            user.is_admin = is_admin
            db.session.commit()
            db.session.refresh(user)
            print(f"Updated admin status for user '{user.username}' to {is_admin}")
        else:
            print(f"No user found with email {email}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Update admin status for a user.')
    parser.add_argument('email', type=str, help='Email of the user')
    parser.add_argument('is_admin', type=int, help='1 to set user as admin, 0 to remove admin status')

    args = parser.parse_args()
    make_admin(args.email, bool(args.is_admin))