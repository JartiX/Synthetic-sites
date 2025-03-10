import sys
import os.path
sys.path.append(
    os.path.abspath(os.path.join(os.path.dirname(__file__), os.path.pardir)))


from models.user_model import db, User, bcrypt
from app import app

def create_user(username: str, email: str, password: str, is_admin: bool):
    """Создание пользователя

    Args:
        username (str): Имя пользователя
        email (str): Почта
        password (str): Пароль
        is_admin (bool): Статус администратора
    """
    with app.app_context():
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        user = User(username=username, email=email, password=hashed_password, is_admin=is_admin)
        db.session.add(user)
        db.session.commit()
        print(f'User {username} created!')

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='Create an admin user.')
    parser.add_argument('username', type=str, help='Username for the admin user')
    parser.add_argument('email', type=str, help='Email for the admin user')
    parser.add_argument('password', type=str, help='Password for the admin user')
    parser.add_argument('is_admin', type=int, help='1 - admin, 0 - not admin')

    args = parser.parse_args()
    create_user(args.username, args.email, args.password, bool(args.is_admin))
