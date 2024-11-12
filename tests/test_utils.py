import pytest

from src.utils import filter_vacanices_by_keywords, get_top_n_vacaninces, get_vacancies_by_salary, instances_to_dicts


def test_get_top_n_vacancies(vacancy1, vacancy2, vacancy3, vacancy4):
    vacancies_list = [vacancy1, vacancy2, vacancy3, vacancy4]
    result = get_top_n_vacaninces(vacancies_list, 2)
    assert result == [vacancy3, vacancy4]


def test_if_top_n_gt_len_vacanices(vacancy1, vacancy2, vacancy3, vacancy4):
    vacancies_list = [vacancy1, vacancy2, vacancy3, vacancy4]
    result = get_top_n_vacaninces(vacancies_list, 5)
    assert result == [vacancy4, vacancy3, vacancy2, vacancy1]


def test_filter_vacanices_by_keywords(vacancy1, vacancy2):
    vacancies_list = [vacancy1, vacancy2]
    result = filter_vacanices_by_keywords(vacancies_list, ["requirement1"])
    assert result == [vacancy1]


def test_get_vacanices_by_salary(vacancy1, vacancy2, vacancy3):
    vacancies_list = [vacancy1, vacancy2, vacancy3]
    result1 = get_vacancies_by_salary(vacancies_list, "1500-3000")
    result2 = get_vacancies_by_salary(vacancies_list, "1500 - 3000")
    assert result1 == [vacancy2, vacancy3]
    assert result2 == [vacancy2, vacancy3]


def test_get_vacancies_by_salary_failure(vacancy1):
    with pytest.raises(TypeError):
        get_vacancies_by_salary([vacancy1], "1")


def test_instance_to_dicts(vacancy1):
    result = instances_to_dicts([vacancy1])
    assert result == [
        {"name": "name1", "employer": "employer1", "url": "url1", "salary": 1000, "requirement": "requirement1"}
    ]
