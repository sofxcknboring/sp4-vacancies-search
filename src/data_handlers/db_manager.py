from typing import List, Tuple

import psycopg2

from src.interfaces import DataConnector
from src.vacancy import Vacancy


class DBManager(DataConnector):
    """
    Args:
        db_name (str): Имя базы данных, к которой необходимо подключиться.
        user (str): Имя пользователя для подключения к базе данных
        password (str): Пароль для подключения к базе данных
        host (str, optional): Хост, на котором запущен сервер базы данных
            По умолчанию 'localhost'.
        port (str, optional): Порт, на котором запущен сервер базы данных
            По умолчанию '5432'.
    Attributes:
        connection (psycopg2.extensions.connection): Объект подключения к базе данных
        cursor (psycopg2.extensions.cursor): Объект курсора для выполнения SQL-запросов
    """

    def __init__(self, db_name, user, password, host="localhost", port="5432"):
        self.db_name = db_name
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.__create_database()
        self.connection = psycopg2.connect(dbname=db_name, user=user, password=password, host=host, port=port)
        self.cursor = self.connection.cursor()
        self.__create_tables()

    def __create_database(self) -> None:
        """
        Создает базу данных, если не существует.
        :return: None
        """
        conn = psycopg2.connect(user=self.user, password=self.password, host=self.host, port=self.port)
        conn.autocommit = True
        cursor = conn.cursor()
        try:
            cursor.execute(f"CREATE DATABASE {self.db_name}")
            cursor.close()
            conn.close()
        except psycopg2.errors.DuplicateDatabase:
            cursor.close()
            conn.close()

    def __create_tables(self) -> None:
        """
        Создает таблицы если не существуют.
        :return: None
        """
        create_employers_table = """
        CREATE TABLE IF NOT EXISTS employers (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL
        );
        """

        create_vacancies_table = """
        CREATE TABLE IF NOT EXISTS vacancies (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) NOT NULL,
            url VARCHAR(255) UNIQUE,
            requirement VARCHAR(255),
            salary NUMERIC,
            employer_id INTEGER REFERENCES employers(id)
        );
        """
        self.cursor.execute(create_employers_table)
        self.cursor.execute(create_vacancies_table)
        self.connection.commit()

    def add_employer(self, employer_id: int, name: str):
        """
        Добавить работодателя.
        """
        query = """
        INSERT INTO employers (id, name) VALUES (%s, %s)
        ON CONFLICT (id) DO NOTHING;
        """
        self.cursor.execute(query, (employer_id, name))
        self.connection.commit()

    def get_data(self):
        query = """
                SELECT employers.name, vacancies.*
                FROM vacancies
                JOIN employers ON vacancies.employer_id = employers.id;
                """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def add_data(self, vacancy: Vacancy):
        check_vacancy_query = "SELECT id FROM vacancies WHERE url = %s;"
        self.cursor.execute(check_vacancy_query, (vacancy.url,))
        existing_vacancy = self.cursor.fetchone()

        if existing_vacancy is not None:
            return

        insert_vacancy_query = """
            INSERT INTO vacancies (name, employer_id, url, salary, requirement)
            VALUES (%s, %s, %s, %s, %s);
        """
        self.cursor.execute(
            insert_vacancy_query, (vacancy.name, vacancy.employer, vacancy.url, vacancy.salary, vacancy.requirement)
        )
        self.connection.commit()

    def delete_data(self, vacancy):
        pass

    def get_employers_and_vacancies_count(self) -> List[Tuple[str, int]]:
        """
        Получить компании и количество вакансий
        :return: List[Tuple[str, int]]
        """
        query = """
        SELECT employers.name, COUNT(vacancies.id) AS vacancies_count
        FROM employers
        LEFT JOIN vacancies ON employers.id = vacancies.employer_id
        GROUP BY employers.name;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_all_vacancies(self) -> List[Tuple[str, int]]:
        """
        Получить все вакансии.
        :return: List[Tuple[str, int]]
        """
        query = """
        SELECT employers.name, vacancies.name, vacancies.salary, vacancies.url
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.id;
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_avg_salary(self) -> str:
        """
        Получить среднюю зарплату по вакансиям
        :return: str
        """
        query = "SELECT AVG(salary) FROM vacancies;"
        self.cursor.execute(query)
        avg_salary = self.cursor.fetchone()[0]
        return f"Средняя зарплата по вакансиям: {avg_salary} руб."

    def get_vacancies_with_higher_salary(self) -> List[Tuple[str, int]]:
        """
        Получить вакансии у которых заплата выше среднего значения.
        :return: List[Tuple[str, int]]
        """
        query = """
        SELECT employers.name, vacancies.name, vacancies.salary, vacancies.url
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.id
        WHERE vacancies.salary > (SELECT AVG(salary) FROM vacancies);
        """
        self.cursor.execute(query)
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword) -> List[Tuple[str, int]]:
        """
        Получить вакансии по ключевому слову в поле name.
        :return: List[Tuple[str, int]]
        """
        query = """
        SELECT employers.name, vacancies.name, vacancies.salary, vacancies.url
        FROM vacancies
        JOIN employers ON vacancies.employer_id = employers.id
        WHERE vacancies.name ILIKE %s;
        """
        self.cursor.execute(query, (f"%{keyword}%",))
        return self.cursor.fetchall()
