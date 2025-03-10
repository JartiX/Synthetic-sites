import json
import time
from keys import api_key, secret_key
import requests
import base64


class GenerateError(Exception):
    pass


class ModelError(Exception):
    pass


class ImageGenerator:
    """Класс для генерации изображений

    Raises:
        GenerateError: Ошибка генерации
        ModelError: Ошибка при получении модели
    """
    URL = None
    AUTH_HEADERS = None

    def __init__(self, url: str, api_key: str, secret_key: str):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        """Функция для получения генеративной модели

        Raises:
            GenerateError: Ошибка генерации

        Returns:
            int: ID модели
        """
        try:
            response = requests.get(
                self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        except Exception as ex:
            raise ModelError(str(ex))
            
        data = response.json()
        return data[0]['id']

    def generate(self, prompt: str, model: int, style="UHD", negativePrompt="", images=1, width=1920, height=1080):
        """Функция для запроса на генерацию

        Args:
            prompt (str): Промпт
            model (int): ID модели
            style (str, optional): Стиль изображения. Defaults to "UHD".
            negativePrompt (str, optional): Отрицательный промпт. Defaults to "".
            images (int, optional): Количество изображений. Defaults to 1.
            width (int, optional): Длина изображения. Defaults to 1920.
            height (int, optional): Высота изображения. Defaults to 1080.

        Raises:
            Generate_error: Ошибка генерации

        Returns:
            str: ID запроса
        """
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "style": style,
            "negativePromptUnclip": negativePrompt,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        
        try:
            response = requests.post(
                self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        except Exception as ex:
            raise GenerateError(str(ex))
        
        data = response.json()
        if "model_status" in data.keys():
            if data["model_status"] == "DISABLED_BY_QUEUE":
                raise GenerateError("Высокая нагрузка на сервис, повторите попытку позже")
        return data['uuid']

    def check_generation(self, request_id: str, attempts=10, delay=10):
        """Функция для получения изображения

        Args:
            request_id (str): ID запроса
            attempts (int, optional): Количество попыток. Defaults to 10.
            delay (int, optional): Задержка между запросами. Defaults to 10.

        Raises:
            GenerateError: Ошибка генерации

        Returns:
            list[str]: Изображения
        """
        while attempts > 0 or data['status'] != "FAIL":
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
        raise GenerateError(data['status'])




def gen_img(prompt: str, path: str, save=False, negative_prompt=""):
    """Основная функция для генерации изображения

    Args:
        prompt (str): Промпт
        path (str): Путь сохранения
        save (bool, optional): Необходимость сохранения. Defaults to False.
        negative_prompt (str, optional): Негативный промпт. Defaults to "".

    Returns:
        bytes: Изображение
    """
    api = ImageGenerator('https://api-key.fusionbrain.ai/',
                        api_key, secret_key)
    model_id = api.get_model()
    __uuid = api.generate(prompt, model_id, negativePrompt=negative_prompt)
    images = api.check_generation(__uuid)
    image_data = base64.b64decode(images[0])
    if save:
        try:
            with open(path, "wb") as file:
                file.write(image_data)
        except:
            with open(path, "w+") as file:
                file.write(image_data)
    return image_data