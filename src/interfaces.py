from abc import ABC, abstractmethod



class ApiHandler(ABC):
    """
        Абстрактный класс для обработки API.
        Класс определяет интерфейс для работы с API, включая методы
        для подключения к API и получения вакансий.
    """

    @abstractmethod
    def connect(self):
        """Метод для подключения к API"""
        pass

    @abstractmethod
    def fetch_data(self, keyword: str):
        """
        Метод для получения вакансий по ключевому слову.
        Args:
            keyword (str): Ключевое слово для поиска вакансий.
        Returns:
            list: Список вакансий, соответствующих ключевому слову.
        """
        pass



class FileHandler(ABC):
    """
    Абстрактный класс для обработки файлов.
    Класс определяет интерфейс для работы с файлами, включая методы
    для получения, добавления и удаления данных.
    """
    @abstractmethod
    def get_data(self):
        """Метод получения данных из файла."""
        pass

    @abstractmethod
    def add_data(self, vacancy):
        """
        Метод добавления данных в файл.
        Args:
            vacancy: Данные вакансии, которые необходимо добавить в файл.
        """
        pass

    @abstractmethod
    def delete_data(self, vacancy):
        """
        Метод удаления данных из файла.
        Args:
            vacancy: Данные вакансии, которые необходимо удалить из файла.
        """
        pass