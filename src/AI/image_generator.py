import json
import time
from keys import api_key, secret_key
import requests
import base64


class Generate_error(Exception):
    pass


class Image_Generator:
    URL = None
    AUTH_HEADERS = None

    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        try:
            response = requests.get(
                self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        except Exception as ex:
            raise Generate_error(str(ex))
            
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, style="UHD", negativePrompt="", images=1, width=1920, height=1080):
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
            raise Generate_error(str(ex))
        
        data = response.json()
        if "model_status" in data.keys():
            if data["model_status"] == "DISABLED_BY_QUEUE":
                raise Generate_error("Высокая нагрузка на сервис, повторите попытку позже")
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0 or data['status'] != "FAIL":
            response = requests.get(
                self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
        raise Generate_error(data['status'])




def gen_img(prompt, path, save=False, negative_prompt=""):
    api = Image_Generator('https://api-key.fusionbrain.ai/',
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


# if __name__ == "__main__":
#     gen_img("city. castle. forest. night. Picture is map of field. Top-view. In the bottom-right corner a river and bridge to farm. to the left relatively to the farm - city(approx 100 pixels left). Upper relatively farm - mountains(approx 300 pixels up). In the top-left corner a magic gates with green shine. In the top-right corner a big castle surrounded river. In the another places - wild forest")
