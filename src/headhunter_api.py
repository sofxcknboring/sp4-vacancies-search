from typing import List

import requests
from src.interfaces import ApiHandler


class HeadHunterAPI(ApiHandler):
    """
        Класс для взаимодействия с API HeadHunter.
        Класс предоставляет методы для выполнения запросов к API HeadHunter,
        включая проверку соединения с сервером.

        Attributes:
            __base_url (str): Базовый URL для запросов к API HeadHunter.
    """
    def __init__(self):
        self.__base_url = "https://api.hh.ru/vacancies/"

    def __connect(self) -> bool:
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()

            return True

        except requests.exceptions.RequestException as req_error:
            print(f'Connection error: {req_error}')
            return False


    def connect(self):
        """
        Проверяет соединение с API HeadHunter.
        Returns:
            bool: Результат проверки соединения (True или False).
        """
        return self.__connect()


    def fetch_data(self, query, area='113') -> List:
        """
        Получение вакансий по запросу.
        :param query: Ключевое слово.
        :param area: '113' -> Россия
        :return: Список всех вакансий.
        """
        if self.connect():
            params = {
                'text': query,
                'search_field': 'name',
                'per_page': 100,
                'page': 0,
                'area': area
            }
            response = requests.get(self.__base_url, params=params)
            return response.json().get('items')

        return []
