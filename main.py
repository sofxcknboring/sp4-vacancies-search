import os

from dotenv import load_dotenv

from src.data_handlers.db_manager import DBManager
from src.data_handlers.json_saver import JsonSaver
from src.headhunter_api import HeadHunterAPI
from src.utils import print_employers, print_vacancies
from src.vacancy import Vacancy

hh_api = HeadHunterAPI()

load_dotenv()

# Получение значений переменных окружения
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


json_saver = JsonSaver()
db_manager = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)

employer_ids = [80, 1740, 4181, 4219, 1373, 39305, 3388, 15478, 4233, 78638]


def main():
    api_con_question = int(input("1. Обратиться к HeadHunter API?\n2. Запросить данные из БД\nВвод:"))
    if api_con_question == 1:
        print("Пожалуйста, подождите...")
        for employer_id in employer_ids:
            name = hh_api.fetch_employers_data(employer_id=employer_id)
            db_manager.add_employer(employer_id=employer_id, name=name)
            vacancies_objects = Vacancy.cast_to_object_list(hh_api.fetch_vacancy_by_employer(employer_id=employer_id))
            for vacancy in vacancies_objects:
                # uncomment if you want
                # json_saver.add_data(vacancy)
                db_manager.add_data(vacancy)
    print("Запрос к API выполнен успешно.")
    flag = True
    while flag:
        new_action = int(
            input(
                """
1. Получить список всех компаний.
2. Получить список всех вакансий.
3. Средняя зарплата по вакансиям.
4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5. Получить вакансии по ключевому слову в названии.
6. Завершить работу скрипта.
"""
            )
        )
        if new_action == 1:
            employers = db_manager.get_employers_and_vacancies_count()
            print_employers(employers)
        elif new_action == 2:
            print("Список всех вакансий:")
            vacancies = db_manager.get_all_vacancies()
            print_vacancies(vacancies)
        elif new_action == 3:
            print(db_manager.get_avg_salary())
        elif new_action == 4:
            print("Вакансии с зарплатой выше средней:")
            higher_salary_vacancies = db_manager.get_vacancies_with_higher_salary()
            print_vacancies(higher_salary_vacancies)
        elif new_action == 5:
            keyword = input("Введите ключевое слово для поиска вакансий: ")
            print(f"Вакансии по ключевому слову '{keyword}':")
            keyword_vacancies = db_manager.get_vacancies_with_keyword(keyword)
            print_vacancies(keyword_vacancies)
        elif new_action == 6:
            flag = False
        else:
            print("Неверный выбор. Пожалуйста, выберите снова.")


if __name__ == "__main__":
    main()
