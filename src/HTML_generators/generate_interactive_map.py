import os
from src.patterns import Patterns
def generate_interactive_map(objects: list, path: str, file_name: str):
    """Создание интерактивной карты

    Args:
        objects (list): Локации
        path (str): Путь сохранения
        file_name (str): Имя файла
    """
    data = []
    for obj in objects:
        data.append(
            {
                "name": obj.name,
                "category": obj.category,
                "coords": obj.coords,
                "id": obj.id
            }
        )

    html = Patterns.get_interactive_map(data=data)
    
    if not os.path.exists(path):
        os.mkdir(path)
    with open(f"{path}/{file_name}", 'w', encoding="utf-8") as file:
        file.write(html)
