import json
import os
from typing import List

from src.interfaces import DataConnector
from src.vacancy import Vacancy


class JsonSaver(DataConnector):
    """
    Класс для обработки JSON файлов.
    Аргументы:
        filename: имя файла(по умолчанию 'vacancies.json').
    """

    def __init__(self, filename="vacancies.json"):
        self.__filename = os.path.join(os.path.dirname(__file__), "../..", "data", filename)
        if not os.path.exists(self.__filename):
            with open(f"{self.__filename}", "w") as file:
                json.dump([], file)

    def get_data(self) -> List:
        """
        Возвращает список данных добавленных ранее.
        :return: List
        """
        try:
            with open(self.__filename, "r") as file:
                vacancies = json.load(file)
                if not isinstance(vacancies, list):
                    return []
                return vacancies
        except json.JSONDecodeError:
            print("Ошибка декодирования JSON. Файл может быть поврежден.")
            return []

    def add_data(self, vacancy: Vacancy) -> None:
        """
        Добавляет новую вакансию в JSON-файл, если такой вакансии еще нет.

        Метод загружает текущие данные из файла, проверяет, есть ли уже вакансия в списке.
        Если такой вакансии нет, она добавляется в список, и файл перезаписывается с обновленными данными.
        Если вакансия уже существует, добавление не происходит.

        Args:
            vacancy (Vacancy): Экземпляр класса Vacancy.(название, URL, зарплата и требования).

        """
        vacancies = self.get_data()

        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "requirement": vacancy.requirement,
        }

        if vacancy_dict not in vacancies:
            vacancies.append(vacancy_dict)
        else:
            print("already in")

        with open(self.__filename, "w") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)

    def delete_data(self, vacancy: Vacancy) -> None:
        """
        Удаляет вакансию из JSON-файла, если она существует.

        Метод загружает текущие данные из файла, проверяет наличие вакансии в списке.
        Если вакансия найдена, она удаляется из списка, и файл перезаписывается с обновленными данными.
        Если вакансия не найдена, выводится соответствующее сообщение.
        """
        vacancies = self.get_data()

        vacancy_dict = {
            "name": vacancy.name,
            "url": vacancy.url,
            "salary": vacancy.salary,
            "requirement": vacancy.requirement,
        }

        if vacancy_dict in vacancies:
            vacancies.remove(vacancy_dict)
            print(vacancies)
        else:
            print("Вакансия не найдена")

        with open(self.__filename, "w") as file:
            json.dump(vacancies, file, ensure_ascii=False, indent=4)
