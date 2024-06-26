from g4f import Model
from g4f.client import Client
from g4f import Provider

class Generate_error(Exception):
    pass


class Text_Generator():
    __model: Model = None
    __provider = None
    __api_key: str = None

    def __init__(self, model, provider, api_key=None):
        if not isinstance(model, Model):
            raise Generate_error("Invalid model")

        self.__model = model
        self.__provider = provider
        self.__api_key = api_key

    def generate(self, prompt, role):
        client = Client(
            provider=self.__provider,
            api_key=self.__api_key
        )
        if not isinstance(prompt, str):
            raise Generate_error("Invalid prompt")
        
        message = [
            {"role": "user", "content": prompt},
            {"role": "system", "content": f"Ты {role}"}
        ]
        try:
            responce = client.chat.completions.create(
                model=self.__model,
                messages=message)
            
        except Exception as ex:
            raise Generate_error(ex)
        
        answer = responce.choices[0].message.content

        if self.__provider == Provider.Blackbox:
            answer = answer[answer.find("rv2$@$")+6:]

        return answer
