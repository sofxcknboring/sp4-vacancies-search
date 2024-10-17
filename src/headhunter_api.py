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

    def _connect(self) -> requests.Response:
        """
            Проверка подключения к API.
            :return: Объект, который содержит ответ сервера на HTTP-запрос.
        """
        try:
            response = requests.get(self.__base_url)
            response.raise_for_status()
            return response
        except requests.exceptions.RequestException as e:
            raise Exception(f'Ошибка подключения к API: {str(e)}')

    def fetch_data(self, query, area='113') -> List[dict]:
        """
        Получение вакансий по запросу.
        :param query: Ключевое слово.
        :param area: '113' -> Россия
        :return: Список всех вакансий.
        """
        try:
            self._connect()
            params = {
                'text': query,
                'search_field': 'name',
                'per_page': 100,
                'page': 0,
                'area': area
            }
            response = requests.get(self.__base_url, params=params)
            response.raise_for_status()
            return response.json().get('items', [])
        except requests.exceptions.RequestException as e:
            print(f'Ошибка получения данных: {str(e)}')
            return []

