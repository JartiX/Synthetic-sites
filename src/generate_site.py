import os
import random
import math
import json
import time

from src.AI.text_generator import TextGenerator
from src.AI.image_generator import gen_img
from src.AI.gemini_text_gen import generate_text

from src.HTML_generators.generate_interactive_map import generate_interactive_map
from src.HTML_generators.generate_html import generate_html
from src.HTML_generators.update_main_html import update_main_html

from models.location_model import LocationModel

from src.constants import Constants


def calculate_distance(coord1: list, coord2: list) -> float:
    """Вычисление дистанции между двумя локациями

    Args:
        coord1 (list): Координаты первой локации
        coord2 (list): Координаты второй локации

    Returns:
        float: Расстояние между локациями
    """
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def generate_random_coordinates(lower: int, upper: int) -> list:
    """Генерация случайных координат

    Args:
        lower (int): Нижний порог координат
        upper (int): Верхний порог координат

    Returns:
        list: Координаты X,Y
    """
    return [
        round(random.uniform(lower, upper), 6), 
        round(random.uniform(lower, upper), 6)
    ]

def are_too_close(coord: list, selected_objects: list, min_distance=20) -> bool:
    """Проверка на близость координат

    Args:
        coord (list): Координаты
        selected_objects (list): Список локаций
        min_distance (int, optional): Минимальная дистанция между локациями. Defaults to 20.

    Returns:
        bool: Результат проверки
    """
    for obj in selected_objects:
        if calculate_distance(coord, obj.coords) < min_distance:
            return True
    return False


def generate_coordinates_with_retries(selected_objects: list, max_attempts=150) -> list:
    """Генерация координат для локации с учетом минимальной дистанции

    Args:
        selected_objects (list): Список локаций
        max_attempts (int, optional): Максимальное число попыток. Defaults to 150.

    Returns:
        list: Координаты
    """
    for _ in range(max_attempts):
        coord = generate_random_coordinates(Constants.lower_coord, Constants.upper_coord)
        if not are_too_close(coord, selected_objects):
            return coord
    return None 


def add_object_to_selected(name: str, category: str, coord: list) -> LocationModel:
    """Создание модели локации

    Args:
        name (str): Имя локации
        category (str): Категория локации
        coord (list): Координаты локации

    Returns:
        LocationModel: Модель локации
    """
    return LocationModel(
        name=name,
        coords=coord,
        category=category,
        image_path=f"static/imgs/{category}/{name}.jpg",
        reviews_path=f"{Constants.path_to_reviews_folder}/{category}/{name}.json",
        description_path=f"{Constants.path_to_description_folder}/{category}/{name}.json"
    )
    
    
def choose_objects(number_of_objects: int, types_of_objects: dict, randomize=True) -> list:
    """Выбор локаций

    Args:
        number_of_objects (int): Количество обьектов
        types_of_objects (dict): Словарь с локациями
        randomize (bool, optional): Необходимость рандомизации. Defaults to True.

    Returns:
        list: Список с локациями LocationModel
    """
    selected_objects = []
    if randomize:
        used_types = {i:0 for i in types_of_objects.keys()}

        while len(selected_objects) < number_of_objects:
            available_types = [
                type_ for type_, used in used_types.items() 
                if used <= number_of_objects / len(used_types.keys())
            ]
            
            if not available_types:
                break

            selected_type = random.choice(available_types)
            object_name = random.choice(types_of_objects[selected_type])
            
            for obj in selected_objects:
                while obj.name == object_name:
                    object_name = random.choice(types_of_objects[selected_type])

            coord = generate_coordinates_with_retries(selected_objects)
                
            if coord:
                selected_objects.append(add_object_to_selected(object_name, selected_type, coord))
                used_types[selected_type] += 1
    else:
        while len(selected_objects) < number_of_objects:
            for type in types_of_objects:
                for object_name in types_of_objects[type]:
                    coord = generate_coordinates_with_retries(selected_objects)
                
                    if coord:
                        selected_objects.append(add_object_to_selected(object_name, type, coord))

    return selected_objects
        
def generate_image(prompt: str, _path=None, save=True, negative_prompt="") -> bytes:
    """Генерация изображения

    Args:
        prompt (str): Промпт
        _path (_type_, optional): Путь сохранения. Defaults to None.
        save (bool, optional): Необходимость сохранения. Defaults to True.
        negative_prompt (str, optional): Отрицательный промпт. Defaults to "".

    Raises:
        Exception: _description_

    Returns:
        bytes: Изображение
    """
    if save and not _path:
        raise Exception("There is not path for save")
    while True:
        try:
            return gen_img(prompt=prompt, save=save, 
                           path=_path, negative_prompt=negative_prompt)
        except Exception as ex:
            print(f"{str(ex)}. Continue...")
            continue

def generate_feedback(prompt: str, category: str, rate: int | str, role: str) -> str:
    """Генерация отзыва

    Args:
        prompt (str): Промпт
        category (str): Категория локации
        rate (int | str): Оценка локации
        role (str): Роль рецензента

    Returns:
        str: Сгенерированный отзыв
    """

    base_prompts = Constants.get_feedback_prompts(role=role,category=category,
                                              prompt=prompt, rate=rate)
    while True:
        try:
            base_prompt = random.choice(base_prompts)
            generated = generate_text(base_prompt, f'{role} который хочет написать отзыв')
            return generated
        except Exception as ex:
            print(ex)
            continue
        
        
def generate_description(prompt: str, category: str) -> str:
    """Генерация описания

    Args:
        prompt (str): Промпт
        category (str): Категория локации

    Returns:
        str: Сгенерированное описание
    """
    while True:
        try:
            base_prompt = Constants.get_description_prompt(prompt=prompt, category=category)
            generated = generate_text(base_prompt, "Чат бот")

            return generated
        except Exception as ex:
            print(ex)
            continue
        
def generate_date(lower_date: int, upper_date: int) -> str:
    """Генерация даты

    Args:
        lower_date (int): Нижний порог
        upper_date (int): Верхний порог

    Returns:
        str: Сгенерированная дата
    """
    # date (list): [day_of_week, month, day_of_month, HH:MM:SS, year]
    date = time.ctime(random.randint(lower_date, upper_date)).split()
    date[0] = Constants.days_dict[date[0]]
    date[1] = Constants.months_dict[date[1]]
    date = f"{date[2]} {date[1]} {date[4]}, {date[0]} {date[3]}"
    
    return date

def generate_feedbacks(object_name: str, category: str, path: str) -> dict:
    """Генерация всех отзывов локации

    Args:
        object_name (str): Имя локации
        category (str): Категория локации
        path (str): Путь сохранения

    Returns:
        dict: Словарь отзывов
    """
    reviews = []
    
    for rating in range(1, 6):
        for _ in range(2):
            role = random.choice(Constants.roles)
            reviews.append(generate_feedback(object_name, category, rating, role))

    json_str = json.dumps(reviews, indent=4, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json_str)
        
    return json.loads(json_str)

def save_data(site_name: str, selected_objects: list) -> None:
    """Сохранение данных сайта

    Args:
        site_name (str): Имя сайта
        selected_objects (list): Список локаций

    Raises:
        Exception: _description_
    """
    data = [
        {
            "name": object.name,
            "coords": object.coords,
            "category": object.category,
            "id": object.id,
            "likes": object.likes,
            "reviews": object.reviews,
            "visits": object.visits,
            "description": object.description
        } for object in selected_objects
    ]
    
    file_path = f'{Constants.path_to_sites_folder}/{site_name}/data.json'
    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(json_str)
            print("Data saved successfully!")
    except Exception as ex:
        raise Exception(f"Unexpected error while saving data! Error: {str(ex)}")


def generate_city_image(priority_generate: bool, city_name: str, categories_names: list) -> None:
    """Генерация изображения города

    Args:
        priority_generate (bool): Приоритет генерации
        city_name (str): Название города
        categories_names (list): Названия локаций
    """
    if priority_generate:
        print("Generating city image...")
        generate_image(
            prompt=f"You must to generate city that named {city_name}. Top-view. In the city placed these key objects: {categories_names}. The main purpose - generate city. Buildings. Architecture",
            _path=f"{Constants.path_to_cities_folder}/{city_name}.jpg",
            save=True,
            negative_prompt="flowers. picture without city. flower"
        )
    else:
        city_image_path = f'{Constants.path_to_cities_folder}/{city_name}.jpg'
        if not os.path.exists(city_image_path):
            print("City image not found! Generating...")
            generate_image(
                prompt=f"You must to generate city that named {city_name}. Top-view. In the city placed these key objects: {categories_names}. The main purpose - generate city. Buildings. Architecture",
                _path=city_image_path,
                save=True,
                negative_prompt="flowers. picture without city. flower"
            )
            print("City image successfully generated!")
            

def process_object_reviews(obj: LocationModel, num: int, selected_objects: list, priority_generate: bool) -> tuple[int, list]:
    """Обработка отзывов локаций

    Args:
        obj (LocationModel): Локация 
        num (int): Номер локации
        selected_objects (list): Список локаций
        priority_generate (bool): Приоритет генерации

    Returns:
        tuple[int, list]: Оценка и список локаций
    """
    selected_objects[num].likes = 0
    feedback = None
    
    if not os.path.exists(f'{Constants.path_to_reviews_folder}/{obj.category}'):
        os.mkdir(f'{Constants.path_to_reviews_folder}/{obj.category}')
        
    if not priority_generate:
        is_reviews_exists = False
        if os.path.exists(obj.reviews_path):
            with open(obj.reviews_path, "r", encoding="utf-8") as f:
                feedback = json.load(f)
            is_reviews_exists = True
        
    sum_rate = 0
    random_choose = []
    for i in range(3):
        rate = random.randint(1, 5)
        role = random.choice(Constants.roles)
        
        date = generate_date(lower_date=Constants.lower_date, upper_date=int(time.time()))
        
        attempts = 0
        if priority_generate:
            selected_objects[num].reviews.append(
                [generate_feedback(obj.name, obj.category, rate, role), rate, date]
            )
        else:
            if not is_reviews_exists:
                feedback = generate_feedbacks(obj.name, obj.category, obj.reviews_path)
                is_reviews_exists = True
            
            index = random.randint(0, len(feedback) - 1)
            while index in random_choose:
                if attempts > 5:
                    break
                
                index = random.randint(0, len(feedback) - 1)
                attempts += 1

            rate = Constants.reviews_rating_by_index[index]
            selected_objects[num].reviews.append(
                [feedback[index], rate, date]
            )
            random_choose.append(index)

        sum_rate += rate

        selected_objects[num].likes += random.randint(Constants.likes[rate][0], Constants.likes[rate][1])
        
    print(f"Reviews for {obj.name} generated.")
    return sum_rate, selected_objects


def process_object_description(obj: LocationModel, num: int, selected_objects: list, priority_generate: bool, sum_rate: int) -> list:
    """Генерация описания

    Args:
        obj (LocationModel): Локация
        num (int): Номер локации
        selected_objects (list): Список локаций
        priority_generate (bool): Приоритет генерации
        sum_rate (int): Рейтинг локации

    Returns:
        list: Список локаций
    """
    if not os.path.exists(f'{Constants.path_to_description_folder}/{obj.category}'):
        os.mkdir(f'{Constants.path_to_description_folder}/{obj.category}')
        
    is_description_exists = False
    
    if not priority_generate:
        if os.path.exists(obj.description_path):
            with open(obj.description_path, "r", encoding="utf-8") as f:
                description = json.load(f)
            is_description_exists = True

    if priority_generate:
        description = generate_description(obj.name, obj.category)
        
        with open(obj.description_path, "w", encoding="utf-8") as f:
            json_str = json.dumps(description, ensure_ascii=False, indent=4)
            f.write(json_str)
            
    else:
        if not is_description_exists:
            description = generate_description(obj.name, obj.category)
            
            with open(obj.description_path, "w", encoding="utf-8") as f:
                json_str = json.dumps(description, ensure_ascii=False, indent=4)
                f.write(json_str)
                
    selected_objects[num].description = description
    print(f"Description for {obj.name} generated.")
            
    selected_objects[num].visits = {
        "monday": random.randint(sum_rate * 20, sum_rate * 30),
        "tuesday": random.randint(sum_rate * 20, sum_rate * 30),
        "wednesday": random.randint(sum_rate * 20, sum_rate * 30),
        "thursday": random.randint(sum_rate * 20, sum_rate * 30),
        "friday": random.randint(sum_rate * 20, sum_rate * 30),
        "saturday": random.randint(sum_rate * 20, sum_rate * 30),
        "sunday": random.randint(sum_rate * 20, sum_rate * 30)
    }

    return selected_objects

          
def generate_site(
    site_name: str, city_name: str, 
    types_of_objects: dict[str, list], 
    min_max_objects: list[int, int], 
    priority_generate=False, randomize=True
) -> None:
    """Функция для генерации сайта

    Args:
        site_name (str): Название сайта
        city_name (str): Название города
        types_of_objects (dict[str, list]): Словарь локаций
        min_max_objects (list[int, int]): Границы минимального и максимального количества локаций
        priority_generate (bool, optional): Приоритет генерации. Defaults to False.
        randomize (bool, optional): Нужна ли рандомизация. Defaults to True.
    """
    number_of_objects = random.randint(min_max_objects[0], min_max_objects[1])
    print(types_of_objects)
    print("Counting all locations...")
    
    number_of_all_objects = 0
    for i in types_of_objects:
        for j in types_of_objects[i]:
            number_of_all_objects += 1
    print(f"Number of locations: {number_of_all_objects}")
    
    selected_objects = choose_objects(
        number_of_objects=number_of_objects if randomize else number_of_all_objects,
        types_of_objects=types_of_objects,
        randomize=randomize
    )
        
    print(f"Number of chosen locations: {number_of_objects}")
    
    print("Generating interactive map...")
    generate_interactive_map(
        selected_objects, 
        f"{Constants.path_to_sites_folder}/{site_name}", 
        file_name="interactive_map.html"
    )
    
    categories_names = []
    for obj in selected_objects:
        if obj.category not in categories_names:
            categories_names.append(obj.category)
    
    categories_names = list({obj.category for obj in selected_objects})
    generate_city_image(priority_generate, city_name, categories_names)
            
    print("Generating reviews and descriptions...")
    for num, obj in enumerate(selected_objects):
        sum_rate, selected_objects = process_object_reviews(
            obj, num, selected_objects, priority_generate
        )
        selected_objects = process_object_description(
            obj, num, selected_objects, priority_generate, sum_rate
        )
    
    print("Saving data...")
    save_data(site_name=site_name, selected_objects=selected_objects)
    
    for obj in selected_objects:
        if not os.path.exists(f'static/imgs/{obj.category}'):
            os.mkdir(f'static/imgs/{obj.category}')
    
    remainders = number_of_objects
    if priority_generate:
        print("Generating images...")
        for obj in selected_objects:
            generate_image(prompt=f"{obj.category}. {obj.name}",_path=obj.image_path,save=True)  
            print(f"Image for {obj.name} generated. Remained {remainders}")
            remainders -= 1
    else:
        for obj in selected_objects:
            if not os.path.exists(obj.image_path):
                print(f"Image for {obj.name} not found! Generating...")
                generate_image(prompt=f"{obj.category}. {obj.name}",_path=obj.image_path,save=True)  
                print(f"Image for {obj.name} generated.")
    
    print("Generating html...")
    html = generate_html(city_name=city_name, selected_objects=selected_objects, site_name=site_name)
    print("html successfully generated!")
    
    with open(f"{Constants.path_to_sites_folder}/{site_name}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Updating sites data...")
    if not os.path.exists(Constants.path_to_sites_data):
        with open(Constants.path_to_sites_data, 'w', encoding="utf-8") as f:
            json_str = json.dumps({site_name:city_name}, ensure_ascii=False, indent=4)
            f.write(json_str)
    else:
        with open(Constants.path_to_sites_data, 'r', encoding="utf-8") as f:
            json_str = json.load(f)
            json_str[site_name] = city_name

        with open(Constants.path_to_sites_data, 'w', encoding="utf-8") as f:
            json_str = json.dumps(json_str, ensure_ascii=False, indent=4)
            f.write(json_str)
            
    print("Data successfully updated!")
    
    print("Updating main form...")
    update_main_html(path="static")
    print("Main form successfully updated!")
            
    