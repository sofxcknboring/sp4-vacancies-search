from src.data_handlers.db_manager import DBManager
from src.data_handlers.json_saver import JsonSaver
from src.headhunter_api import HeadHunterAPI
from src.utils import get_top_n_vacaninces, print_vacancies, print_employers
from src.vacancy import Vacancy
import os
from dotenv import load_dotenv
hh_api = HeadHunterAPI()

load_dotenv()

# Получение значений переменных окружения
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
DB_HOST = os.getenv('DB_HOST')
DB_PORT = os.getenv('DB_PORT')


json_saver = JsonSaver()
db_manager = DBManager(DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT)


def main():
    api_con_question = int(input("1. Обратиться к HeadHunter API?\n2. Запросить данные из БД\nВвод:"))
    if api_con_question == 1:
        search_query = input("Введите поисковый запрос: ")
        top_n = int(input("Введите количество вакансий для вывода в топ N: "))

        vacanices_objects = Vacancy.cast_to_object_list(hh_api.fetch_data(search_query))
        top_n_vacancies = get_top_n_vacaninces(vacanices_objects, top_n)

        for vacancy in top_n_vacancies:
            # uncomment if you want
            # json_saver.add_data(vacancy)
            db_manager.add_data(vacancy)
    flag = True
    while flag:
        new_action = int(
            input(
                """
1. Получить список всех компаний.
2. Получить список всех вакансий.
3. Средняя зарплата по вакасиям.
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
