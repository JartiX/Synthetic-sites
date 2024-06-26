from flask import send_from_directory, redirect, url_for, request, render_template, flash, jsonify
from flask_login import login_user, current_user, logout_user, login_required
from functools import wraps
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import json
import os
from src.auth_scripts.forms import RegistrationForm, LoginForm
from src.delete_site import delete_site
from src.HTML_generators.update_main_html import update_main_html
from src.generate_site import generate_site
from models.user_model import db, bcrypt, User
from app import app
from src.auth_scripts.create_user import create_user

limiter = Limiter(
    key_func=get_remote_address,
    default_limits=["10 per minute"]
)

limiter.init_app(app)

def make_error(ex, error_code):
    json_text = json.dumps({"details": str(ex)},
                            sort_keys=True, indent=4,  ensure_ascii=False)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text}",
        status=error_code,
        mimetype="application/json; charset=utf-8"
    )
    
    return result

def make_responce(text):
    if isinstance(text, (str, int, float)):
        text = {"responce": text}
        
    json_text = json.dumps(text,
                            sort_keys=True, indent=4,  ensure_ascii=False)

    # Подготовить ответ
    result = app.response_class(
        response=f"{json_text}",
        status=200,
        mimetype="application/json; charset=utf-8"
    )
    
    return result

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
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
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


@app.route('/api/<site>/get_locations/', methods=['GET'])
def get_locations(site):
    '''
    Returns:
        [
            {
                "id": Идентификатор локации (str)
                "name": Название локации (str)
                "category": Категория локации (str)
            },
            ...
        ]
    '''
    try:
        result = []
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                result.append(
                    {
                        "id": location["id"],
                        "name": location["name"],
                        "category": location["category"]
                    }
                )
                    
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
      
@app.route('/api/<site>/get_likes_by_id/', methods=['GET'])
def get_likes_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        {
            "likes": число лайков (int)
        }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = {
                        "likes": location['likes']
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
        
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
    
@app.route('/api/<site>/get_visits_by_id/', methods=['GET'])
def get_visits_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        "visits"
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
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = location['visits']
                    break
        if result is None:
            return make_error("Location not found", 404)
                    
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
     
@app.route('/api/<site>/get_reviews_by_id/', methods=['GET'])
def get_reviews_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        "reviews"
            [
                [
                    "review": отзыв (str),
                    "rating": рейтинг (int),
                    "date": дата отзыва (str)
                ],
                ...
            ]
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = location["reviews"]
                    break
        if result is None:
            return make_error("Location not found", 404)
                    
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
    
@app.route('/api/<site>/get_stats_by_id/', methods=['GET'])
def get_stats_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        "stats"
            {
                "reviews": отзывы (list),
                "visits": посещаемость (dict),
                "likes": число лайков (int)
            }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = {
                        "reviews": location["reviews"],
                        "visits": location["visits"],
                        "likes": location["likes"]
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
                    
        return make_responce(result)
    
    except Exception as ex:
        return make_error(ex, 500)

@app.route('/api/<site>/get_name_by_id/', methods=['GET'])
def get_name_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        {
            "name": название локации (str)
        }
    """ 
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = {
                        "name": location["name"]
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
        
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
    
@app.route('/api/<site>/get_category_by_id/', methods=['GET'])
def get_category_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        {
            "category": название категории (str)
        }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = {
                        "type": location["category"]
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
        
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)

@app.route('/api/<site>/get_location_id_by_name/', methods=['GET'])
def get_location_id_by_name(site):
    """
    Args: 
        "site": имя сайта (str)
        "name": название локации (str)
    Returns:
        {
            "id": идентификатор локации (str)
        }
    """
    name = request.args.get("name")
    if name is None:
        return make_error("Not enought params. Expected params: name" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["name"] == name:
                    result = {
                        "id": location["id"]
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
        
        return make_responce(result)
                
    except Exception as ex:
        return make_error(ex, 500)
    
@app.route('/api/<site>/get_average_visits_by_id/', methods=['GET'])
def get_average_visits_by_id(site):
    """
    Args: 
        "site": имя сайта (str)
        "id": идентификатор локации (str)
    Returns:
        {
            "avg_visits": среднее число посещений (int)
        }
    """
    id = request.args.get("id")
    if id is None:
        return make_error("Not enought params. Expected params: id" ,403)
    
    try:
        result = None
        
        with open(f'static/sites/{site}/data.json', 'r', encoding="utf-8") as f:
            data = json.load(f)
            for location in data:
                if location["id"] == id:
                    result = {
                        "avg_visits":(sum([i for i in location['visits'].values()]))/7
                    }
                    break
        if result is None:
            return make_error("Location not found", 404)
        
        return make_responce(result)
                
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
    """
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
        
        return make_responce("User successfully deleted!")
        
    except Exception as ex:
        return make_error(str(ex), 500)    

@app.route('/api/create_user', methods=['POST'])
@admin_required
def create_user_api():
    """
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
        return make_error("Not enough params. Expected params: username, email, password. Optional params: is_admin", 403)
    if is_admin is None:
        is_admin = False
        
    try:
        is_admin = bool(int(is_admin))
    except ValueError:
        return make_error("Invalid value for is_admin. Expected 0 or 1", 402)
    
    try:
        create_user(username, email, password, is_admin)
        return make_responce(f"User {username} created successfully!")
    except Exception as ex:
        return make_error(str(ex), 500)

@app.route('/api/make_admin_by_id', methods=['PUT'])
@admin_required
def make_admin_by_id():
    """
    Args:
        id (str): id пользователя,
        is_admin (bool): статус администратора,
        API-KEY (str): индивидуальный API-ключ
    """
    id = request.args.get("id")
    is_admin = request.args.get("is_admin")
    
    if id is None:
        return make_error("Not enough params. Expected params: id. Optional params: is_admin", 403)
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
        
        return make_responce(f"Updated admin status for user '{user.username}' to {is_admin}")
    
    except Exception as ex:
        return make_error(str(ex), 500)


@app.route('/api/get_username_by_id', methods=['GET'])
@admin_required
def get_username_by_id():
    """
    Args:
        id (str): идентификатор пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
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
        
        return make_responce({"username": user.username})
    
    except Exception as ex:
        return make_error(str(ex), 500)
    
@app.route('/api/get_email_by_id', methods=['GET'])
@admin_required
def get_email_by_id():
    """
    Args:
        id (str): идентификатор пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
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
        
        return make_responce({"email": user.email})
    
    except Exception as ex:
        return make_error(str(ex), 500)

@app.route('/api/get_id_by_username', methods=['GET'])
@admin_required
def get_id_by_username():
    """
    Args:
        username (str): имя пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
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
        
        return make_responce({"id": user.id})
    
    except Exception as ex:
        return make_error(str(ex), 500)

@app.route('/api/get_id_by_email', methods=['GET'])
@admin_required
def get_id_by_email():
    """
    Args:
        email (str): email пользователя,
        API-KEY (str): индивидуальный API-ключ
    Returns:
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
        
        return make_responce({"id": user.id})
    
    except Exception as ex:
        return make_error(str(ex), 500)

@app.route('/api/get_users', methods=['GET'])
@admin_required
def get_users():
    """
    Returns:
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
            make_error("Not enough params. Expected params: page. Optional params: per_page", 403)
        
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
            'users': [{'id': user.id, 'username': user.username, 'email': user.email} for user in users.items]
        }
        
        return make_responce(result)
    
    except Exception as ex:
        return make_error(str(ex), 500)
    
# Удалить сайт только из главной страницы
@app.route('/api/delete_site_from_main_page/', methods=['DELETE'])
@admin_required
def delete_site_from_main_page():
    """
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            API-KEY (str): индивидуальный API-ключ
        
    """
    site = request.args.get("site")
    if site is None:
        return make_error("Not enought params. Expected params: site" ,403)
    
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
        
    return make_responce("Site successfully deleted!")
        
        
# Добавить уже существующий сайт на главную страницу
@app.route('/api/add_existed_site/', methods=['POST', 'PUT'])
@admin_required
def add_existed_site():
    """
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            city (str): название города,
            API-key (str): индивидуальный API-ключ 
    """
    city = request.args.get("city")
    site = request.args.get("site")
    if city is None or site is None:
        return make_error("Not enought params. Expected params: city, site" ,403)

    if not os.path.exists('static/sites.json'):
        with open('static/sites.json', 'w', encoding='utf-8') as f:
            sites = json.dumps({site:city}, ensure_ascii=False, indent=4)
            f.write(sites)
        update_main_html("static")
            
        return make_responce("Site successfully added!")
    
    with open('static/sites.json', 'r', encoding='utf-8') as f:
        sites = json.load(f)
        if site in sites:
            return make_error(f"Site already exists: {site}:{sites[site]}", 406)
        
        sites[site] = city 
    
    with open('static/sites.json', 'w', encoding='utf-8') as f:
        sites = json.dumps(sites, ensure_ascii=False, indent=4)
        f.write(sites)
        
    update_main_html("static")
           
    return make_responce("Site successfully added!")
    
    
# Полное удаление сайта
@app.route('/api/delete_site/', methods=['DELETE'])
@admin_required
def delete_site_():
    """
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            API-key (str): индивидуальный API-ключ 
    """
    site = request.args.get("site")
    if site is None:
        return make_error("Not enought params. Expected params: site" ,403)

    if not os.path.exists('static/sites.json'):
        return make_error('Error. Data file not found!', 404)
    
    try:
        delete_site(site)
    except Exception as ex:
        return make_error(str(ex), 500)
    
    return make_responce("Site successfully deleted!")

# Сгенерировать сайт и добавить его на главную страницу
@app.route('/api/create_site/', methods=['POST'])
@admin_required
def create_site():
    """
        Для доступа к функции требуются админ права и API-ключ
        Args:
            site (str): название сайта,
            city (str): название города,
            types_of_objects (dict[str:list]): список необходимых обьектов в формате
            категория обьектов:список обьектов,
            min_max_objects (list(int, int), tuple(int, int)): границы количества выбранных обьектов,
            priority_generate (0/1): указание приоритета генерации контента,
            randomize (0/1): нужно ли выбирать случайное число обьектов или создавать сайт со всеми обьектами,
            API-key (str): индивидуальный API-ключ 
    """
    city = request.args.get("city")
    site = request.args.get("site")
    types_of_objects = request.args.get("types_of_objects")
    min_max_objects = request.args.get("min_max_objects")
    priority_generate = request.args.get("priority_generate")
    randomize = request.args.get("randomize")
    
    if city is None or site is None or types_of_objects is None or min_max_objects is None:
        return make_error("Not enought params. Expected params: city:str, site:str, types_of_objects:dict[str, list], min_max_objects:list[int, int] | tuple(int, int). Optional params: priority_generate:0/1, randomize:0/1" ,403)

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
        generate_site(site_name=site, city_name=city, types_of_objects=types_of_objects, min_max_objects=min_max_objects, priority_generate=priority_generate, randomize=randomize)
        return make_responce("Site successfully generated and added to main page")
    
    except Exception as ex:
        return make_error(ex, 500)

    
if __name__ == "__main__":
    app.run(debug=True)