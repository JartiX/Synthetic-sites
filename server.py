from flask import (
    send_from_directory, redirect, url_for, request, 
    render_template, flash, jsonify
)
from flask_login import (
    login_user, current_user, logout_user, login_required
)
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

from functools import wraps
import json
import os
import textwrap

from app import app
from src.auth_scripts.forms import RegistrationForm, LoginForm
from models.user_model import db, bcrypt, User
from src.auth_scripts.create_user import create_user

from src.delete_site import delete_site
from src.HTML_generators.update_main_html import update_main_html
from src.generate_site import generate_site

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

limiter.init_app(app)


def make_error(ex: str, error_code: int):
    """Вспомогательная функция для создания ответа с ошибкой

    Returns:
        Responce: ответ
    """
    json_text = json.dumps({"details": str(ex)}, sort_keys=True, 
                           indent=4,  ensure_ascii=False)

    return app.response_class(
        response=f"{json_text}",
        status=error_code,
        mimetype="application/json; charset=utf-8"
    )


def make_response(text: str):
    """Вспомогательная функция для создания успешного ответа

    Returns:
        Responce: ответ
    """
    if isinstance(text, (str, int, float)):
        text = {"responce": text}

    json_text = json.dumps(text,
                           sort_keys=True, indent=4,  ensure_ascii=False)

    return app.response_class(
        response=f"{json_text}",
        status=200,
        mimetype="application/json; charset=utf-8"
    )


def load_locations_data(site: str):
    """Вспомогательная функция для загрузки данных локаций

    Raises:
        Exception: Ошибка при попытке загрузить данные с сайта

    Returns:
        dict: данные локаций
    """
    try:
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            return json.load(f)
    except Exception as ex:
        raise Exception(f"Ошибка при попытке загрузить данные с {site}: {ex}")
    
    
@app.route("/templates/home.html")
@app.route("/templates/home")
def home():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('home.html')


@app.route("/templates/register.html", methods=['GET', 'POST'])
@app.route("/templates/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(
            form.password.data
        ).decode('utf-8')
        
        user = User(username=form.username.data,
                    email=form.email.data, password=hashed_password)
        
        db.session.add(user)
        db.session.commit()
        flash('Ваш аккаунт был успешно создан!', 'success')
        
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)


@app.route("/templates/login.html", methods=['GET', 'POST'])
@app.route("/templates/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('dashboard'))
        else:
            flash('Неверный email-адрес или пароль!', 'danger')
            
    return render_template('login.html', form=form)


@app.route("/templates/logout.html")
@app.route("/templates/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/templates/dashboard.html")
@app.route("/templates/dashboard")
@login_required
def dashboard():
    return render_template('dashboard.html', api_key=current_user.api_key)


@app.route('/templates/admin_panel')
@app.route('/templates/admin_panel.html')
@login_required
def admin_panel():
    return render_template('admin_panel.html', api_key=current_user.api_key)


@app.route('/')
def index():
    return redirect(url_for('static_files', filename='main_page.html'))


@app.route('/static/<path:filename>/')
def static_files(filename):
    return send_from_directory('static', filename)


def get_location_by_id(site: str, location_id: int) -> dict:
    """Вспомогательная функция для получения локации по ID
    
    Args:
        site (str): имя сайта
        location_id (int): ID локации
        
    Returns:
        dict: данные локации
    """
    locations_data = load_locations_data(site)
    for location in locations_data:
        if location["id"] == location_id:
            return location
    return None


@app.route('/api/<site>/get_locations/', methods=['GET'])
def get_locations(site: str) -> list:
    """Вспомогательная функция для получения всех локаций

    Args:
        site (str): имя сайта

    Returns:
        list: locations_data
    """
    try:
        result = [
            {
                "id": location["id"],
                "name": location["name"],
                "category": location["category"]
            } for location in load_locations_data(site)
        ]
        
        return make_response(result)

    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_likes_by_id/', methods=['GET'])
def get_likes_by_id(site: str) -> dict:
    """Получить лайки по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации 
        
    Returns:
        dict: лайки локации
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        
        return make_response({"likes": location['likes']})

    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_visits_by_id/', methods=['GET'])
def get_visits_by_id(site: str) -> dict:
    """Получить посещения по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации
         
    Returns:
        dict: 
            {
                "friday": int,
                "monday": int,
                "saturday": int,
                "sunday": int,
                "thursday": int,
                "tuesday": int,
                "wednesday": int
            }
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        return make_response(location['visits'])
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_reviews_by_id/', methods=['GET'])
def get_reviews_by_id(site: str) -> list:
    """Получить отзывы по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации 
    Returns:
        list:
            [
                [
                    "review": отзыв (str),
                    "rating": рейтинг (int),
                    "date": дата отзыва (str)
                ],
                ...
            ]
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        return make_response(location["reviews"])
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_stats_by_id/', methods=['GET'])
def get_stats_by_id(site: str) -> dict:
    """Получить статистику по ID локации
    Args: 
        site (str): имя сайта 
        id: идентификатор локации (str)
    Returns:
        dict:
            {
                "reviews": отзывы (list),
                "visits": посещаемость (dict),
                "likes": число лайков (int)
            }
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        
        result = {
            "reviews": location["reviews"],
            "visits": location["visits"],
            "likes": location["likes"]
        }
        return make_response(result)
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_name_by_id/', methods=['GET'])
def get_name_by_id(site: str) -> dict:
    """Получить имя по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации
    Returns:
        dict:
        {
            "name": название локации (str)
        }
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        return make_response({"name": location["name"]})
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_category_by_id/', methods=['GET'])
def get_category_by_id(site: str) -> dict:
    """Получить категорию по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации 
    Returns:
        dict:
        {
            "type": название категории (str)
        }
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)
        return make_response({"type": location["category"]})
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_locations_by_category_name', methods=['GET'])
def get_locations_by_category_name(site: str) -> dict:
    """Получить локацию по названию категории
    Args:
    site (str): имя сайта 
    category (str): название категории
    Returns:
    dict:
    {
        "locations": [
            {
            "id": идентификатор локации (str),
            "name": название локации (str),
            }
        ]
    }
    """
    category = request.args.get("category")
    if category is None:
        return make_error("Not enought params. Expected params: category", 403)

    try:
        result = [
            {"id": location["id"], "name": location["name"]}
            for location in load_locations_data(site)
            if location["category"] == category
        ]

        if not result:
            return make_error(f"There are no locations with category {category}", 404)
        
        return make_response(result)
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_location_id_by_name/', methods=['GET'])
def get_location_id_by_name(site: str) -> dict:
    """Получить локацию по названию локации
    Args: 
        site (str): имя сайта 
        name (str): название локации
    Returns:
        dict:
        {
            "id": идентификатор локации (str)
        }
    """
    name = request.args.get("name")
    if name is None:
        return make_error("Not enought params. Expected params: name", 403)

    try:
        location = next((
            loc for loc in load_locations_data(site) if loc["name"] == name), 
            None
        )

        if not location:
            return make_error("Location not found", 404)
        
        return make_response({"id": location["id"]})
    
    except Exception as ex:
        return make_error(ex, 500)


@app.route('/api/<site>/get_average_visits_by_id/', methods=['GET'])
def get_average_visits_by_id(site: str) -> dict:
    """Получить среднюю посещаемость по ID локации
    Args: 
        site (str): имя сайта 
        id (str): идентификатор локации
    Returns:
        dict:
        {
            "avg_visits": среднее число посещений (int)
        }
    """
    location_id = request.args.get("id")
    if location_id is None:
        return make_error("Not enought params. Expected params: id", 403)

    try:
        location = get_location_by_id(site, location_id)
        if not location:
            return make_error("Location not found", 404)

        avg_visits = sum(location['visits'].values()) / 7
        return make_response({"avg_visits": avg_visits})
    
    except Exception as ex:
        return make_error(ex, 500)


def admin_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        api_key = request.args.get('API-KEY')
        if not api_key:
            return make_error("Missing API-KEY", 401)

        user = User.query.filter_by(api_key=api_key).first()
        if not user:
            return make_error("Invalid API-KEY", 402)

        if not user.is_admin:
            return make_error("Admin access required", 405)

        return f(*args, **kwargs)

    return wrap


@app.route('/api/remove_user_by_id', methods=['DELETE'])
@admin_required
def remove_user_by_id():
    """Удалить пользователя по ID
    Args:
        id (str): идентификатор пользователя,
        API-KEY (str): индивидуальный API-ключ
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enough params. Expected params: id", 403)

    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_error("User not found", 404)
        
        db.session.delete(user)
        db.session.commit()

        return make_response("User successfully deleted!")

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/create_user', methods=['POST'])
@admin_required
def create_user_api():
    """Создать пользователя
    Args:
        username (str): имя пользователя,
        email (str): email пользователя,
        password (str): пароль пользователя,
        is_admin (int): права администратора (0 или 1),
        API-KEY (str): индивидуальный API-ключ
    """
    username = request.args.get("username")
    email = request.args.get("email")
    password = request.args.get("password")
    is_admin = request.args.get("is_admin")

    if not username or not email or not password:
        return make_error(
            "Not enough params. Expected params: username, email, password. Optional params: is_admin", 403
        )
    
    if is_admin is None:
        is_admin = False

    try:
        is_admin = bool(int(is_admin))
    except ValueError:
        return make_error("Invalid value for is_admin. Expected 0 or 1", 402)

    try:
        create_user(username, email, password, is_admin)
        return make_response(f"User {username} created successfully!")
    
    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/make_admin_by_id', methods=['PUT'])
@admin_required
def make_admin_by_id():
    """Изменить статус администрирования пользователя по ID
    Args:
        id (str): id пользователя,
        is_admin (bool): статус администратора,
        API-KEY (str): индивидуальный API-ключ
    """
    id = request.args.get("id")
    is_admin = request.args.get("is_admin")

    if id is None:
        return make_error(
            "Not enough params. Expected params: id. Optional params: is_admin", 403
        )
    
    if is_admin is None:
        is_admin = False
        
    try:
        is_admin = bool(int(is_admin))
    except ValueError:
        return make_error("Invalid value for is_admin. Expected 0 or 1.", 402)

    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_error("User not found", 404)

        user.is_admin = is_admin
        db.session.commit()
        db.session.refresh(user)

        return make_response(
            f"Updated admin status for user '{user.username}' to {is_admin}"
        )

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_username_by_id', methods=['GET'])
@admin_required
def get_username_by_id() -> dict:
    """Получить пользователя по ID
    Args:
        id (str): идентификатор пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
        dict:
        {
            "username": имя пользователя (str)
        }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enough params. Expected params: id", 403)

    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_error("User not found", 404)

        return make_response({"username": user.username})

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_email_by_id', methods=['GET'])
@admin_required
def get_email_by_id() -> dict:
    """Получить email пользователя по ID
    Args:
        id (str): идентификатор пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
        dict:
        {
            "email": email пользователя (str)
        }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enough params. Expected params: id", 403)

    try:
        user = User.query.filter_by(id=id).first()
        if not user:
            return make_error("User not found", 404)

        return make_response({"email": user.email})

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_id_by_username', methods=['GET'])
@admin_required
def get_id_by_username() -> dict:
    """Получить ID пользователя по имени
    Args:
        username (str): имя пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
        dict:
        {
            "id": идентификатор пользователя (str)
        }
    """
    username = request.args.get("username")
    if username is None:
        return make_error("Not enough params. Expected params: username", 403)

    try:
        user = User.query.filter_by(username=username).first()
        if not user:
            return make_error("User not found", 404)

        return make_response({"id": user.id})

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_id_by_email', methods=['GET'])
@admin_required
def get_id_by_email() -> dict:
    """Получить ID пользователя по email
    Args:
        email (str): email пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
        dict:
        {
            "id": идентификатор пользователя (str)
        }
    """
    email = request.args.get("email")
    if email is None:
        return make_error("Not enough params. Expected params: email", 403)

    try:
        user = User.query.filter_by(email=email).first()
        if not user:
            return make_error("User not found", 404)

        return make_response({"id": user.id})

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_users', methods=['GET'])
@admin_required
def get_users() -> dict:
    """Получить список пользователей
    Returns:
    dict:
    {
        "users": [
            {
                "id": идентификатор пользователя (str),
                "username": имя пользователя (str),
                "email": электронная почта пользователя (str)
            },
                ...
                ],
        "total": количество пользователей (int),
        "pages": количество страниц (int),
        "current_page": текущая страница (int),
        "per_page": количество пользователей на странице (int)
    """
    try:
        page = request.args.get('page', type=int)
        per_page = request.args.get('per_page', type=int)

        if page is None:
            make_error(
                "Not enough params. Expected params: page. Optional params: per_page", 403)

        if per_page is None:
            per_page = 10

        elif per_page > 100:
            per_page = 100

        users = User.query.paginate(page=page, per_page=per_page)

        result = {
            'total': users.total,
            'pages': users.pages,
            'current_page': users.page,
            'per_page': users.per_page,
            'users': [
                {
                    'id': user.id, 
                    'username': user.username, 
                    'email': user.email
                } for user in users.items
            ]
        }

        return make_response(result)

    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/delete_site_from_main_page/', methods=['DELETE'])
@admin_required
def delete_site_from_main_page():
    """Удалить сайт только из главной страницы.
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            API-KEY (str): индивидуальный API-ключ

    """
    site = request.args.get("site")
    if site is None:
        return make_error("Not enought params. Expected params: site", 403)

    if not os.path.exists('static/sites.json'):
        return make_error('Error. Data file not found!', 404)

    with open('static/sites.json', 'r', encoding='utf-8') as f:
        try:
            sites = json.load(f)
            if site not in sites:
                return make_error("Site already deleted", 406)

            del sites[site]
            f.seek(0)

        except Exception as ex:
            return make_error(ex, 500)

    with open('static/sites.json', 'w', encoding='utf-8') as f:
        sites = json.dumps(sites, ensure_ascii=False, indent=4)
        f.write(sites)

    update_main_html("static")

    return make_response("Site successfully deleted!")


@app.route('/api/add_existed_site/', methods=['POST', 'PUT'])
@admin_required
def add_existed_site():
    """Добавить уже существующий сайт на главную страницу.
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            city (str): название города,
            API-KEY (str): индивидуальный API-ключ 
    """
    city = request.args.get("city")
    site = request.args.get("site")
    if city is None or site is None:
        return make_error("Not enought params. Expected params: city, site", 403)

    if not os.path.exists('static/sites.json'):
        with open('static/sites.json', 'w', encoding='utf-8') as f:
            sites = json.dumps({site: city}, ensure_ascii=False, indent=4)
            f.write(sites)
            
        update_main_html("static")

        return make_response("Site successfully added!")

    with open('static/sites.json', 'r', encoding='utf-8') as f:
        sites = json.load(f)
        if site in sites:
            return make_error(f"Site already exists: {site}:{sites[site]}", 406)

        sites[site] = city

    with open('static/sites.json', 'w', encoding='utf-8') as f:
        sites = json.dumps(sites, ensure_ascii=False, indent=4)
        f.write(sites)

    update_main_html("static")

    return make_response("Site successfully added!")


@app.route('/api/delete_site/', methods=['DELETE'])
@admin_required
def delete_site_():
    """Полное удаление сайта.
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            API-KEY (str): индивидуальный API-ключ 
    """
    site = request.args.get("site")
    if site is None:
        return make_error("Not enought params. Expected params: site", 403)

    if not os.path.exists('static/sites.json'):
        return make_error('Error. Data file not found!', 404)

    try:
        delete_site(site)
    except Exception as ex:
        return make_error(str(ex), 500)

    return make_response("Site successfully deleted!")


@app.route('/api/create_site/', methods=['POST'])
@admin_required
def create_site():
    """Сгенерировать сайт и добавить его на главную страницу.
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            city (str): название города,
            types_of_objects (dict[str:list]): список необходимых обьектов в формате
            категория обьектов:список обьектов,
            min_max_objects (list(int, int), tuple(int, int)): границы количества выбранных обьектов,
            priority_generate (0/1): указание приоритета генерации контента,
            randomize (0/1): нужно ли выбирать случайное число обьектов или создавать сайт со всеми обьектами,
            API-KEY (str): индивидуальный API-ключ 
    """
    city = request.args.get("city")
    site = request.args.get("site")
    types_of_objects = request.args.get("types_of_objects")
    min_max_objects = request.args.get("min_max_objects")
    priority_generate = request.args.get("priority_generate")
    randomize = request.args.get("randomize")

    if city is None or site is None or types_of_objects is None or min_max_objects is None:
        return make_error(
            textwrap.dedent("""
            Not enough params. Expected params: city:str, site:str, 
            types_of_objects: dict[str, list], 
            min_max_objects: list[int, int] | tuple(int, int). 
            Optional params: priority_generate: 0/1, randomize: 0/1
            """),
            403,
        )

    if priority_generate is None:
        priority_generate = False

    if randomize is None:
        randomize = True
    try:
        priority_generate = bool(int(priority_generate))
        randomize = bool(int(randomize))
        types_of_objects = json.loads(types_of_objects)
        min_max_objects = json.loads(min_max_objects)
    except Exception as ex:
        return make_error(ex, 402)

    try:
        generate_site(site_name=site, city_name=city, types_of_objects=types_of_objects,
                      min_max_objects=min_max_objects, priority_generate=priority_generate, randomize=randomize)
        return make_response("Site successfully generated and added to main page")

    except Exception as ex:
        return make_error(ex, 500)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0")
