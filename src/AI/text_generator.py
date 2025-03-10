from g4f import Model
from g4f.client import Client
from g4f import Provider

class GenerateError(Exception):
    pass


class TextGenerator():
    """Класс для генерации текста

    Raises:
        GenerateError: Ошибка генерации
    """
    __model: Model = None
    __provider = None
    __api_key: str = None

    def __init__(self, model: Model, provider: Provider, api_key=None):
        if not isinstance(model, Model):
            raise GenerateError("Invalid model")

        self.__model = model
        self.__provider = provider
        self.__api_key = api_key

    def generate(self, prompt: str, role: str):
        """Функция генерации текста

        Args:
            prompt (str): Промпт
            role (str): Роль

        Raises:
            GenerateError: Ошибка генерации

        Returns:
            str: Сгенерированный текст
        """
        client = Client(
            provider=self.__provider,
            api_key=self.__api_key
        )
        if not isinstance(prompt, str):
            raise GenerateError("Invalid prompt")
        
        message = [
            {"role": "user", "content": prompt},
            {"role": "system", "content": f"Ты {role}"}
        ]
        try:
            responce = client.chat.completions.create(
                model=self.__model,
                messages=message)
            
        except Exception as ex:
            raise GenerateError(ex)
        
        answer = responce.choices[0].message.content

        if self.__provider == Provider.Blackbox:
            answer = answer[answer.find("rv2$@$")+6:]

        return answer
