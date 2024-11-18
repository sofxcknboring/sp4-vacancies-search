import pytest

from src.data_handlers.json_saver import JsonSaver
from src.headhunter_api import HeadHunterAPI
from src.vacancy import Vacancy


@pytest.fixture
def api():
    return HeadHunterAPI()


@pytest.fixture
def vacancy1():
    return Vacancy("name1", {"id": 1}, "url1", {"from": 1000}, "requirement1")


@pytest.fixture
def vacancy2():
    return Vacancy("name2", {"id": 2}, "url2", {"from": 2000}, "requirement2")


@pytest.fixture
def vacancy3():
    return Vacancy("name3", {"id": 3}, "url3", {"from": None, "to": 3000}, "requirement3")


@pytest.fixture
def vacancy4():
    return Vacancy(
        "name4",
        {"id": 4},
        "url4",
        {"from": 3000},
        "<highlighttext>requirement3</highlighttext>",
    )


@pytest.fixture
def vacancies():
    return [
        {
            "name": "name1",
            "employer": {"id": 1},
            "url": "url1",
            "salary": {
                "from": 1000,
            },
            "snippet": {"requirement": "requirement1"},
        },
        {
            "name": "name2",
            "employer": {"id": 2},
            "url": "url2",
            "salary": {
                "to": 2000,
            },
            "snippet": {"requirement": "requirement2"},
        },
    ]


@pytest.fixture
def json_saver():
    return JsonSaver()
