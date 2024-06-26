from uuid import uuid4

class Location_model:
    __name: str = None
    __coords: list[int] = None
    __category: str = None
    __id: uuid4 = None
    __likes: int = None
    __reviews: list = None
    __visits: dict[str, int] = None
    __description: str = None
    __image_path: str = None
    __reviews_path: str = None
    __description_path: str = None
    
    def __init__(self, name, coords, category, image_path, reviews_path, description_path):
        if not isinstance(name, str):
            raise TypeError("Имя должно быть строкой")
        if not isinstance(coords, list):
            raise TypeError("Координаты должны быть списком")
        if not isinstance(category, str):
            raise TypeError("Категория должна быть строкой")
        if not isinstance(image_path, str):
            raise TypeError("Путь до изображения должен быть строкой")
        if not isinstance(reviews_path, str):
            raise TypeError("Путь до отзывов должен быть строкой")
        if not isinstance(description_path, str):
            raise TypeError("Путь до описания должен быть строкой")
        
        self.__name = name
        self.__coords = coords
        self.__category = category
        self.__image_path = image_path
        self.__reviews_path = reviews_path
        self.__description_path = description_path
        
        self.__reviews = []
        self.__visits = {}
        self.__id = uuid4()
        

    # Getter for name
    @property
    def name(self):
        return self.__name

    # Setter for name
    @name.setter
    def name(self, value):
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        self.__name = value

    # Getter for coords
    @property
    def coords(self):
        return self.__coords

    # Setter for coords
    @coords.setter
    def coords(self, value):
        if not isinstance(value, list):
            raise TypeError("Координаты должны быть списком")
        self.__coords = value

    # Getter for category
    @property
    def category(self):
        return self.__category

    # Setter for category
    @category.setter
    def category(self, value):
        if not isinstance(value, str):
            raise TypeError("Категория должна быть строкой")
        self.__category = value

    # Getter for id
    @property
    def id(self):
        return str(self.__id)

    # Getter for likes
    @property
    def likes(self):
        return self.__likes

    # Setter for likes
    @likes.setter
    def likes(self, value):
        if not isinstance(value, int):
            raise TypeError("Лайки должны быть целым числом")
        if value < 0:
            raise ValueError("Лайки не могут быть отрицательными")
        self.__likes = value

    # Getter for reviews
    @property
    def reviews(self):
        return self.__reviews

    # Setter for reviews
    @reviews.setter
    def reviews(self, value):
        if not isinstance(value, list):
            raise TypeError("Отзывы должны быть списком")
        self.__reviews = value

    # Getter for visits
    @property
    def visits(self):
        return self.__visits

    # Setter for visits
    @visits.setter
    def visits(self, value):
        if not isinstance(value, dict):
            raise TypeError("Посещения должны быть словарем")
        self.__visits = value
        
    # Getter for image_path
    @property
    def image_path(self):
        return self.__image_path

    # Setter for image_path
    @image_path.setter
    def image_path(self, value):
        if not isinstance(value, str):
            raise TypeError("Путь до изображения должен быть строкой")
        self.__image_path = value
        
    # Getter for reviews_path
    @property
    def reviews_path(self):
        return self.__reviews_path

    # Setter for reviews_path
    @reviews_path.setter
    def reviews_path(self, value):
        if not isinstance(value, str):
            raise TypeError("Путь до отзывов должен быть строкой")
        self.__reviews_path = value   
        
    # Getter for description_path
    @property
    def description_path(self):
        return self.__description_path

    # Setter for description_path
    @description_path.setter
    def description_path(self, value):
        if not isinstance(value, str):
            raise TypeError("Путь до описания должен быть строкой")
        self.__description_path = value   
        
    # Getter for description
    @property
    def description(self):
        return self.__description

    # Setter for description
    @description.setter
    def description(self, value):
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        self.__description = value   