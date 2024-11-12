import re
from typing import Dict, List, Optional


class Vacancy:
    """
    Класс для работы с вакансиями.

    Атрибуты:
        name (str): Название вакансии.
        employer (str) Работодатель.
        url (str): URL вакансии.
        salary (int): Зарплата вакансии.
        requirement (str): Требования к вакансии.
    """

    __slots__ = ("__name", "__employer", "__url", "__salary", "__requirement")

    def __init__(self, name: str, employer: Optional[Dict], url: str, salary: Optional[Dict], requirement: str):
        self.__name = self.__validate_name(name)
        self.__employer = self.__validate_employer(employer)
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

    @property
    def employer(self):
        return self.__employer

    def __str__(self):
        return f"""
{self.name}
{self.employer}
{self.url}
{self.salary}
{self.requirement}"""

    # Методы валидации.
    @staticmethod
    def __validate_name(name: str) -> str:
        if not isinstance(name, str) or not name:
            return "Не определено"
        return name

    @staticmethod
    def __validate_employer(employer: Optional[Dict]) -> str:
        if not isinstance(employer, dict):
            return "Не определено"
        return employer.get("name")

    @staticmethod
    def __validate_url(url: str) -> str:
        if not isinstance(url, str) or not url:
            return "Не определено"
        return url

    @staticmethod
    def __validate_salary(salary: Optional[Dict]) -> int:
        if not isinstance(salary, dict):
            return 0

        salary_from = salary.get("from")
        salary_to = salary.get("to")
        if salary_from is not None:
            return salary_from
        if salary_to is not None:
            return salary_to

        return 0

    @staticmethod
    def __validate_requirement(requirement: Optional[str]) -> str:
        if not isinstance(requirement, str) or not requirement:
            return "Не определено"
        cleaned_requirement = re.sub(r"<highlighttext>(.*?)</highlighttext>", r"\1", requirement)
        return cleaned_requirement

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
            employer = vacancy.get("employer")
            url = vacancy.get("alternate_url")
            salary = vacancy.get("salary")
            requirement = vacancy.get("snippet").get("requirement")
            obj_list.append(Vacancy(name, employer, url, salary, requirement))
        return obj_list
