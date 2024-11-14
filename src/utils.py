import re
from typing import Dict, List

from src.vacancy import Vacancy


def get_top_n_vacaninces(vacancies: List["Vacancy"], top_n: int) -> List["Vacancy"]:
    """
    Возвращает top_n вакансий по зарплате.
    :param vacancies: (List["Vacancy"]) -> Вакансии.
    :param top_n: (int) -> кол-во вакансий которые нужно вернуть.
    :return: (List["Vacancy"]) -> Список top_n вакансий.
    """
    return sorted(vacancies, reverse=True)[:top_n]


def filter_vacanices_by_keywords(vacancies: List["Vacancy"], filter_words: List) -> List["Vacancy"]:
    """
    Фильтрует вакансии по ключевым словам в requirements (требованиях).
    """
    filter_words_lower = [word.lower() for word in filter_words]

    return [v for v in vacancies if any(word.lower() in v.requirement.lower() for word in filter_words_lower)]


def get_vacancies_by_salary(vacancies: List["Vacancy"], salary_range: str) -> List["Vacancy"]:
    """
    Фильтрует вакансии, оставляя только те которые попадают в переданный диапазон(salary_range).
    :param vacancies: (List["Vacancy"]) -> Вакансии для фильтра.
    :param salary_range: (str) -> Диапазон зарплат. Example("100000-150000")
    :return: List["Vacancy"] -> Отфильтрованный список вакансий.
    """
    match = re.findall(r"(\d+)\s?-\s?(\d+)", salary_range)
    try:
        start = int(match[0][0])
        end = int(match[0][1])
        return [v for v in vacancies if start <= v.salary <= end]
    except (IndexError, ValueError) as e:
        raise TypeError("Ошибка при обработке диапазона зарплат.") from e


def instances_to_dicts(vacanices: List["Vacancy"]) -> List[Dict]:
    """
    Преобразует список экземпляров класса Vacancy в список словарей.

    :param vacanices: (List["Vacancy"]) -> Список экземпляров класса Vacancy.
    :return: (List[Dict]) -> Список словарей, представляющих экземпляры.
    """
    return [
        {
            "name": instance.name,
            "employer": instance.employer,
            "url": instance.url,
            "salary": instance.salary,
            "requirement": instance.requirement,
        }
        for instance in vacanices
    ]


def print_vacancies(vacancies) -> None:
    if not vacancies:
        print("Нет доступных вакансий.")
        return

    for employer_name, vacancy_name, salary, url in vacancies:
        print(f"Компания: {employer_name}")
        print(f"Вакансия: {vacancy_name}")
        print(f"Зарплата: {salary} руб.")
        print(f"Ссылка: {url}")
        print("-" * 40)


def print_employers(employers) -> None:
    if not employers:
        print("Нет доступных работодателей")
        return

    for employer_name, vacanices_count in employers:
        print(f"Компания: {employer_name}")
        print(f"Количество вакансий: {vacanices_count}")
        print("-" * 40)
