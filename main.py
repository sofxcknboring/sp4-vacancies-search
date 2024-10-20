from src.data_handlers.json_saver import JsonSaver
from src.headhunter_api import HeadHunterAPI
from src.utils import filter_vacanices_by_keywords, get_top_n_vacaninces, get_vacancies_by_salary
from src.vacancy import Vacancy

hh_api = HeadHunterAPI()


json_saver = JsonSaver()


def main():
    search_query = input("Введите поисковый запрос: ")
    top_n = int(input("Введите количество вакансий для вывода в топ N: "))
    filter_words = input("Введите ключевые слова для фильтрации вакансий: Example: Django Flask ... ").split()
    salary_range = input("Введите диапазон зарплат (Example: 100000-150000):")

    vacanices_objects = Vacancy.cast_to_object_list(hh_api.fetch_data(search_query))

    filtered_vacancies = filter_vacanices_by_keywords(vacanices_objects, filter_words)

    filtered_vacancies = get_vacancies_by_salary(filtered_vacancies, salary_range)

    top_n_vacancies = get_top_n_vacaninces(filtered_vacancies, top_n)

    for vacancy in top_n_vacancies:
        # uncomment if you want
        # json_saver.add_data(vacancy)
        print(str(vacancy))


if __name__ == "__main__":
    main()
