from uuid import uuid4

class LocationModel:
    """Модель Локации

    Raises:
        TypeError: _description_
    """
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
    
    def __init__(self, name: str, coords: list, category: str, image_path: str, reviews_path: str, description_path: str):
        """Инициализация локационной модели

        Args:
            name (str): Имя локации
            coords (list): Координаты локации
            category (str): Категория
            image_path (str): Путь до изображения
            reviews_path (str): Путь до отзывов
            description_path (str): Путь до описания

        Raises:
            TypeError: Ошибка типа
        """
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
        

    @property
    def name(self):
        """Получить имя локации

        Returns:
            str: Имя локации
        """
        return self.__name

    @name.setter
    def name(self, value: str):
        """Задать имя локации

        Args:
            value (str): Имя локации

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Имя должно быть строкой")
        self.__name = value

    @property
    def coords(self):
        """Получить координаты

        Returns:
            int: Координаты
        """
        return self.__coords

    @coords.setter
    def coords(self, value: list):
        """Задать координаты

        Args:
            value (list): X, Y координаты

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, list):
            raise TypeError("Координаты должны быть списком")
        self.__coords = value

    @property
    def category(self):
        """Получить категорию

        Returns:
            str: Категория
        """
        return self.__category

    @category.setter
    def category(self, value: str):
        """Задать категорию

        Args:
            value (str): Названии категории

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Категория должна быть строкой")
        self.__category = value

    @property
    def id(self):
        """Получить ID локации

        Returns:
            uuid4: ID локации
        """
        return str(self.__id)

    @property
    def likes(self):
        """Получить лайки

        Returns:
            int: Лайки
        """
        return self.__likes

    @likes.setter
    def likes(self, value: int):
        """Задать лайки

        Args:
            value (int): Лайки

        Raises:
            TypeError: _description_
            ValueError: _description_
        """
        if not isinstance(value, int):
            raise TypeError("Лайки должны быть целым числом")
        if value < 0:
            raise ValueError("Лайки не могут быть отрицательными")
        self.__likes = value

    @property
    def reviews(self):
        """Получить отзывы

        Returns:
            list: Отзывы
        """
        return self.__reviews

    @reviews.setter
    def reviews(self, value: list):
        """Задать отзывы

        Args:
            value (list): Отзывы

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, list):
            raise TypeError("Отзывы должны быть списком")
        self.__reviews = value

    @property
    def visits(self):
        """Получить посещения

        Returns:
            dict[str, int]: Посещения
        """
        return self.__visits

    @visits.setter
    def visits(self, value: dict[str, int]):
        """Задать посещения

        Args:
            value (dict[str, int]): Посещения

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, dict):
            raise TypeError("Посещения должны быть словарем")
        self.__visits = value
        
    @property
    def image_path(self):
        """Получить путь до изображения

        Returns:
            str: Путь до изображения
        """
        return self.__image_path

    @image_path.setter
    def image_path(self, value: str):
        """Задать путь до изображения

        Args:
            value (str): Путь до изображения

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Путь до изображения должен быть строкой")
        self.__image_path = value
        
    @property
    def reviews_path(self):
        """Получить путь до отзывов

        Returns:
            str: Путь до отзывов
        """
        return self.__reviews_path

    @reviews_path.setter
    def reviews_path(self, value: str):
        """Задать путь до отзывов

        Args:
            value (str): Путь до отзывов

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Путь до отзывов должен быть строкой")
        self.__reviews_path = value   
        
    @property
    def description_path(self):
        """Получить путь до описания

        Returns:
            str: _description_
        """
        return self.__description_path

    @description_path.setter
    def description_path(self, value: str):
        """Задать путь до описания

        Args:
            value (str): Путь до описаний

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Путь до описания должен быть строкой")
        self.__description_path = value   
        
    @property
    def description(self):
        """Получить описание

        Returns:
            str: Описание
        """
        return self.__description

    @description.setter
    def description(self, value: str):
        """Задать описание

        Args:
            value (str): Описание

        Raises:
            TypeError: _description_
        """
        if not isinstance(value, str):
            raise TypeError("Описание должно быть строкой")
        self.__description = value   