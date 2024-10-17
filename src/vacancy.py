from typing import Dict, List, Optional


class Vacancy:
    """
    Класс для работы с вакансиями.

    Атрибуты:
        name (str): Название вакансии.
        url (str): URL вакансии.
        salary (int): Зарплата вакансии.
        requirement (str): Требования к вакансии.
    """

    __slots__ = ("__name", "__url", "__salary", "__requirement")

    def __init__(self, name: str, url: str, salary: Optional[Dict], requirement: str):
        self.__name = self.__validate_name(name)
        self.__url = self.__validate_url(url)
        self.__salary = self.__validate_salary(salary)
        self.__requirement = self.__validate_requirement(requirement)

    @property
    def name(self):
        return self.__name

    @property
    def url(self):
        return self.__url

    @property
    def salary(self):
        return self.__salary

    @property
    def requirement(self):
        return self.__requirement

    # Методы валидации.
    @staticmethod
    def __validate_name(name: str) -> str:
        if not isinstance(name, str) or not name:
            return "Не определено"
        return name

    @staticmethod
    def __validate_url(url: str) -> str:
        if not isinstance(url, str) or not url:
            return "Не определено"
        return url

    @staticmethod
    def __validate_salary(salary: Optional[Dict]) -> int:
        if salary is None or not isinstance(salary, dict):
            return 0

        if "salary" in salary and isinstance(salary["salary"], dict):
            salary_from = salary["salary"].get("from")
            salary_to = salary["salary"].get("to")

            if salary_from:
                return salary_from
            return salary_to
        return 0

    @staticmethod
    def __validate_requirement(requirement: Optional[str]) -> str:
        if not isinstance(requirement, str) or not requirement:
            return "Не определено"
        return requirement

    def __lt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary < other.salary

    def __le__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary <= other.salary

    def __eq__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary == other.salary

    def __gt__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary > other.salary

    def __ge__(self, other):
        if not isinstance(other, Vacancy):
            return NotImplemented
        return self.salary >= other.salary

    @staticmethod
    def cast_to_object_list(vacancies_list: List[Dict]) -> List["Vacancy"]:
        """
        Преобразует список словарей с данными о вакансиях в список объектов Vacancy.
        Аргументы:
            vacancies_list (List[Dict]): Список словарей с данными о вакансиях.
        Returns:
            List[Vacancy]: Список объектов Vacancy.
        """
        obj_list = []
        for vacancy in vacancies_list:
            name = vacancy.get("name")
            url = vacancy.get("alternate_url")
            salary = vacancy.get("salary")
            requirement = vacancy.get("snippet").get("requirement")
            obj_list.append(Vacancy(name, url, salary, requirement))
        return obj_list
