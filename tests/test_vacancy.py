import pytest

from src.vacancy import Vacancy


def test_init_vacancy(vacancy3):
    assert vacancy3.name == "name3"
    assert vacancy3.employer == "employer3"
    assert vacancy3.url == "url3"
    assert vacancy3.salary == 3000
    assert vacancy3.requirement == "requirement3"


def test_none_vacancy():
    vacancy_with_none = Vacancy(None, None, None, None, None)
    assert vacancy_with_none.name == "Не определено"
    assert vacancy_with_none.employer == "Не определено"
    assert vacancy_with_none.url == "Не определено"
    assert vacancy_with_none.salary == 0
    assert vacancy_with_none.requirement == "Не определено"


def test_salary_comprasion(vacancy1, vacancy2, vacancy3, vacancy4):
    assert vacancy3 > vacancy1
    assert vacancy3 >= vacancy1
    assert vacancy1 < vacancy2
    assert vacancy1 <= vacancy2
    assert vacancy3 == vacancy4


def test_comparison_with_non_vacancy(vacancy1):
    with pytest.raises(Exception):
        assert vacancy1 > 1000


def test_cast_to_object_list(vacanices):
    result = Vacancy.cast_to_object_list(vacanices)
    for vac in result:
        assert isinstance(vac, Vacancy)
