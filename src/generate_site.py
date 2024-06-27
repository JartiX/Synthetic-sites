import os
import random
import math
import json
import time

from src.AI.text_generator import Text_Generator
from src.AI.image_generator import gen_img
from src.AI.gemini_text_gen import generate_text

from src.HTML_generators.generate_interactive_map import generate_interactive_map
from src.HTML_generators.generate_html import generate_html
from src.HTML_generators.update_main_html import update_main_html

from models.location_model import Location_model
from g4f import Provider
from g4f import models


lower_coord, upper_coord = 20, 1080

likes = {
    1: [5, 20],
    2: [20, 35],
    3: [35, 50],
    4: [50, 65],
    5: [65, 80]
}

roles = [
    "ребенок", "мать", "отец", "старик", "студент",
    "бизнесмен", "домохозяйка", "путешественник", "гурман", "геймер",
    "подросток", "пенсионер", "спортсмен", "художник", "любитель музыки",
    "киноман", "книголюб", "технофил", "эколог", "авантюрист",
    "шопоголик", "гастрономический критик", "эксперт по красоте",
    "здоровьесберегающий", "владелец домашних животных", "автолюбитель", "владелец дома"
]


months_dict = {
    "Jan": "Янв",
    "Feb": "Фев",
    "Mar": "Мар",
    "Apr": "Апр",
    "May": "Май",
    "Jun": "Июн",
    "Jul": "Июл",
    "Aug": "Авг",
    "Sep": "Сен",
    "Oct": "Окт",
    "Nov": "Ноя",
    "Dec": "Дек"
}

days_dict = {
    "Mon": "Пн",
    "Tue": "Вт",
    "Wed": "Ср",
    "Thu": "Чт",
    "Fri": "Пт",
    "Sat": "Сб",
    "Sun": "Вс"
}

reviews_rating_by_index = {
    0: 1,
    1: 1,
    2: 2,
    3: 2,
    4: 3,
    5: 3,
    6: 4,
    7: 4,
    8: 5,
    9: 5
}

path_to_cities_folder = "static/imgs/Города"
path_to_reviews_folder = "static/reviews"
path_to_description_folder = "static/descriptions"
path_to_sites_folder = "static/sites"
path_to_sites_data = "static/sites.json"

def distance(coord1, coord2):
    return math.sqrt((coord1[0] - coord2[0])**2 + (coord1[1] - coord2[1])**2)

def generate_random_coordinates(lower, upper):
    return [round(random.uniform(lower, upper), 6), round(random.uniform(lower, upper), 6)]

def are_too_close(coord, selected_objects, min_distance=20):
    for obj in selected_objects:
        if distance(coord, obj.coords) < min_distance:
            return True
    return False

def choose_objects(number_of_objects, types_of_objects, randomize=True):
    selected_objects = []
    if randomize:
        used_types = {i:0 for i in types_of_objects.keys()}

        while len(selected_objects) < number_of_objects:
            available_types = [type_ for type_,
                            used in used_types.items() if used <= number_of_objects/len(used_types.keys())]
            if not available_types:
                break

            type_ = random.choice(available_types)
            object_name = random.choice(types_of_objects[type_])
            for obj in selected_objects:
                while obj.name == object_name:
                    object_name = random.choice(types_of_objects[type_])

            max_attempts = 150

            for _ in range(max_attempts):
                coord = generate_random_coordinates(lower_coord, upper_coord)
                if not are_too_close(coord, selected_objects):
                    # Если координаты достаточно далеко от всех выбранных объектов
                    break
                
            selected_objects.append(Location_model(name=object_name, coords=coord,
                                                   category=type_, image_path=f"static/imgs/{type_}/{object_name}.jpg",
                                                   reviews_path=f"{path_to_reviews_folder}/{type_}/{object_name}.json",
                                                   description_path=f"{path_to_description_folder}/{type_}/{object_name}.json"))
            used_types[type_] += 1
    else:
        while len(selected_objects) < number_of_objects:
            for type in types_of_objects:
                for object_name in types_of_objects[type]:
                    coord = generate_random_coordinates(lower_coord, upper_coord)

                    max_attempts = 150

                    for _ in range(max_attempts):
                        coord = generate_random_coordinates(lower_coord, upper_coord)
                        if not are_too_close(coord, selected_objects):
                            # Если координаты достаточно далеко от всех выбранных объектов
                            break
                
                    selected_objects.append(Location_model(name=object_name, coords=coord, 
                                                           category=type_, image_path=f"static/imgs/{type_}/{object_name}.jpg", 
                                                           reviews_path=f"{path_to_reviews_folder}/{type_}/{object_name}.json", 
                                                           description_path=f"{path_to_description_folder}/{type_}/{object_name}.json"))
 
                       
    return selected_objects
        
def generate_image(prompt, _path=None, save=True, negative_prompt=""):
    if save and not _path:
        raise Exception("There is not path for save")
    while True:
        try:
            return gen_img(prompt=prompt, save=save, path=_path, negative_prompt=negative_prompt)
        except Exception as ex:
            print(f"{str(ex)}. Continue...")
            continue

def generate_feedback(prompt, category, rate, role):

    base_prompts = [
        f"""
            Тебе разрешено писать только на русском
            Твоя роль - {role}. Напиши небольшой отзыв для этой категории - {category} в стиле обычного обывателя.
            Учитывай ключевые аспекты, такие как удобства, сервис, цена и тому подобное (все, чего тебе не хватает, разрешено придумать в зависимости от необходимого рейтинга ( от 1 до 5 звезд)).
            Целевая аудитория – туристы, планирующие отдых.
            Отзывы должны быть информативными и полезными.
            Твоя задача — написать отзыв о {prompt} с оценкой {rate}.
            Предоставь ответ в формате plain text, избегая использования markdown-разметки. Не включай заголовки, списки, ссылки или другие элементы форматирования
            Запрещено писать перевод вашего ответа
            Запрещено писать, что вы ассистент или бот
            """,
            
            f"""
            Тебе разрешено писать только на русском
            Твоя роль - {role}. Напиши всесторонний и детализированный отзыв для этой категории - {category}.
            Учитывай ключевые аспекты, такие как удобства, сервис, цена и тому подобное (все, чего тебе не хватает, разрешено придумать в зависимости от необходимого рейтинга ( от 1 до 5 звезд)).
            Целевая аудитория – туристы, планирующие отдых.
            Отзывы должны быть информативными и полезными.
            Твоя задача — написать отзыв о {prompt} с оценкой {rate}.
            Ты должен дать оценку по всем аспектам.
            Предоставь ответ в формате plain text, избегая использования markdown-разметки. Не включай заголовки, списки, ссылки или другие элементы форматирования
            Запрещено писать перевод вашего ответа
            Запрещено писать, что вы ассистент или бот
            """,
            f"""
            Тебе разрешено писать только на русском
            Твоя роль - {role}. Напиши короткий отзыв для этой категории - {category}.
            Учитывай разные ключевые аспекты (все, чего тебе не хватает, разрешено придумать в зависимости от необходимого рейтинга ( от 1 до 5 звезд)).
            Целевая аудитория – туристы, планирующие отдых.
            Твоя задача — написать отзыв о {prompt} с оценкой {rate}.
            Предоставь ответ в формате plain text, избегая использования markdown-разметки. Не включай заголовки, списки, ссылки или другие элементы форматирования
            Запрещено писать перевод вашего ответа
            Запрещено писать, что вы ассистент или бот
            """,
            f"""
            Тебе разрешено писать только на русском
            Твоя роль - {role}. Напиши короткий отзыв для этой категории - {category}.
            Целевая аудитория – туристы, планирующие отдых.
            Твоя задача — написать отзыв о {prompt} с оценкой {rate}.
            Предоставь ответ в формате plain text, избегая использования markdown-разметки. Не включай заголовки, списки, ссылки или другие элементы форматирования
            Запрещено писать перевод вашего ответа
            Запрещено писать, что вы ассистент или бот
            """
    ]
    while True:
        try:
            base_prompt = random.choice(base_prompts)
            generated = generate_text(base_prompt, f'{role} который хочет написать отзыв')
            return generated
        except Exception as ex:
            print(ex)
            continue
        
        
def generate_description(prompt, category):

    while True:
        try:
            base_prompt = f"""
            Тебе разрешено писать только на русском
            Напиши описание локации {prompt} для этой категории - {category}.
            Не пиши про уникальность места
            Предоставь ответ в формате plain text, избегая использования markdown-разметки. Не включай заголовки, списки, ссылки или другие элементы форматирования
            Запрещено писать перевод вашего ответа
            Запрещено писать, что вы ассистент или бот
            """
            generated = generate_text(base_prompt, "Чат бот")

            return generated
        except Exception as ex:
            print(ex)
            continue
        
def generate_date(lower_date, upper_date):
    date = time.ctime(random.randint(lower_date, upper_date)).split()
    date[0] = days_dict[date[0]]
    date[1] = months_dict[date[1]]
    date = f"{date[2]} {date[1]} {date[4]}, {date[0]} {date[3]}"
    
    return date

def generate_feedbacks(object_name, __type, path):
    reviews = []
    for i in range(2):
        role = random.choice(roles)
        reviews.append(generate_feedback(object_name, __type, 1, role))

        
    for i in range(2):
        role = random.choice(roles)
        reviews.append(generate_feedback(object_name, __type, 2, role))

    for i in range(2):
        role = random.choice(roles)
        reviews.append(generate_feedback(object_name, __type, 3, role))

    for i in range(2):
        role = random.choice(roles)
        reviews.append(generate_feedback(object_name, __type, 4, role))

    for i in range(2):
        role = random.choice(roles)
        reviews.append(generate_feedback(object_name, __type, 5, role))


    json_str = json.dumps(reviews, indent=4, ensure_ascii=False)
    with open(path, "w", encoding="utf-8") as f:
        f.write(json_str)
        
    return json.loads(json_str)

def save_data(site_name, selected_objects):
    data = []
    for object in selected_objects:
        data.append(
            {
                "name": object.name,
                "coords": object.coords,
                "category": object.category,
                "id": object.id,
                "likes": object.likes,
                "reviews": object.reviews,
                "visits": object.visits,
                "description": object.description
            }
        )
    file_path = f'{path_to_sites_folder}/{site_name}/data.json'
    json_str = json.dumps(data, indent=4, ensure_ascii=False)

    try:
        with open(file_path, 'w', encoding="utf-8") as f:
            f.write(json_str)
            print("Data saved successfully!")
    except Exception as ex:
        raise Exception(f"Unexpected error while saving data! Error: {str(ex)}")


def generate_site(site_name: str, city_name: str, types_of_objects: dict[str, list], min_max_objects: list[int, int], priority_generate=False, randomize=True):
    number_of_objects = random.randint(min_max_objects[0], min_max_objects[1])
    print(types_of_objects)
    print("Counting all locations...")
    number_of_all_objects = 0
    for i in types_of_objects:
        for j in types_of_objects[i]:
            number_of_all_objects += 1
    print(f"Number of locations: {number_of_all_objects}")
    
    
    if randomize:
        selected_objects = choose_objects(number_of_objects=number_of_objects, types_of_objects=types_of_objects, randomize=True)
    else:
        selected_objects = choose_objects(number_of_objects=number_of_all_objects, types_of_objects=types_of_objects, randomize=False)
        number_of_objects = number_of_all_objects
        
    print(f"Number of choosed locations: {number_of_objects}")
    
    print("Generating interactive map...")
    generate_interactive_map(selected_objects, 
                             f"{path_to_sites_folder}/{site_name}", 
                             file_name="interactive_map.html")
    
    categories_names = []
    for obj in selected_objects:
        if obj.category not in categories_names:
            categories_names.append(obj.category)
    
    if priority_generate:
        print("Generating city image...")
        generate_image(prompt=f"""You must to generate city that named {city_name}. 
                       Top-view. In the city placed these key objects: {categories_names}. 
                       The main purpose - generate city. Buildings. Architecture""",
                       _path=f"{path_to_cities_folder}/{city_name}.jpg",
                       save=True, negative_prompt="flowers. picture without city. flower")
    else:
        if not os.path.exists(f'{path_to_cities_folder}/{city_name}.jpg'):
            print("City image not found! Generating...")
            generate_image(prompt=f"""You must to generate city that named {city_name}. 
                           Top-view. In the city placed these key objects: {categories_names}. 
                           The main purpose - generate city. Buildings. Architecture""",
                           _path=f"{path_to_cities_folder}/{city_name}.jpg",
                           save=True, negative_prompt="flowers. picture without city. flower")
            print("City image successfully generated!")
            
    lower_date = 1318808725
    upper_date = int(time.time())

    print("Generating reviews and descriptions...")
    remainders = number_of_objects
    for num, obj in enumerate(selected_objects):
        selected_objects[num].likes=0
        feedback = None
        
        if not os.path.exists(f'{path_to_description_folder}/{obj.category}'):
            os.mkdir(f'{path_to_description_folder}/{obj.category}')
            
        if not priority_generate:
            is_reviews_exists = False
            is_description_exists = False
            
            if not os.path.exists(f'{path_to_reviews_folder}/{obj.category}'):
                os.mkdir(f'{path_to_reviews_folder}/{obj.category}')
                
            elif os.path.exists(obj.reviews_path):
                with open(obj.reviews_path, "r", encoding="utf-8") as f:
                    feedback = json.load(f)
                is_reviews_exists = True
                
                
            if os.path.exists(obj.description_path):
                with open(obj.description_path, "r", encoding="utf-8") as f:
                    description = json.load(f)
                is_description_exists = True
                
        sum_rate = 0
        random_choose = []
        for i in range(3):
            rate = random.randint(1,5)
            role = random.choice(roles)
            
            
            date = generate_date(lower_date=lower_date, upper_date=upper_date)
            
            attempts = 0
            if priority_generate:
                selected_objects[num].reviews.append(
                    [generate_feedback(obj.name, obj.category, rate, role), rate, date]
                    )
            else:
                if not is_reviews_exists:
                    feedback = generate_feedbacks(obj.name, obj.category, obj.reviews_path)
                    is_reviews_exists = True
                
                index = random.randint(0, len(feedback)-1)
                while index in random_choose:
                    if attempts > 5:
                        break
                    
                    index = random.randint(0, len(feedback)-1)
                    attempts += 1

                rate = reviews_rating_by_index[index]
                selected_objects[num].reviews.append(
                    [feedback[index], rate, date]
                    )
                random_choose.append(index)

            sum_rate += rate

            selected_objects[num].likes+=random.randint(likes[rate][0],likes[rate][1])
            
        print(f"Reviews for {obj.name} generated. Remained {remainders}")
        
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
        print(f"Description for {obj.name} generated. Remained {remainders}")
                
            
        selected_objects[num].visits = {
            "monday": random.randint(sum_rate*20, sum_rate*30),
            "tuesday": random.randint(sum_rate*20, sum_rate*30),
            "wednesday": random.randint(sum_rate*20, sum_rate*30),
            "thursday": random.randint(sum_rate*20, sum_rate*30),
            "friday": random.randint(sum_rate*20, sum_rate*30),
            "saturday": random.randint(sum_rate*20, sum_rate*30),
            "sunday": random.randint(sum_rate*20, sum_rate*30)
        }
        remainders -= 1
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
    
    with open(f"{path_to_sites_folder}/{site_name}/index.html", "w", encoding="utf-8") as f:
        f.write(html)
    
    print("Updating sites data...")
    if not os.path.exists(path_to_sites_data):
        with open(path_to_sites_data, 'w', encoding="utf-8") as f:
            json_str = json.dumps({site_name:city_name}, ensure_ascii=False, indent=4)
            f.write(json_str)
    else:
        with open(path_to_sites_data, 'r', encoding="utf-8") as f:
            json_str = json.load(f)
            json_str[site_name] = city_name

        with open(path_to_sites_data, 'w', encoding="utf-8") as f:
            json_str = json.dumps(json_str, ensure_ascii=False, indent=4)
            f.write(json_str)
            
    print("Data successfully updated!")
    
    print("Updating main form...")
    update_main_html(path="static")
    print("Main form successfully updated!")
            
    