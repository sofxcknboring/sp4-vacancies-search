from unittest.mock import patch

import pytest
import requests

from src.headhunter_api import HeadHunterAPI


@patch("requests.get")
def test_fetch_data_success(mock_get, api):

    mock_response = requests.Response()
    mock_response.status_code = 200
    mock_response.json = lambda: {"items": [{"key": "1", "next_key": "123"}, {"key": "2", "next_key": "123"}]}

    mock_get.return_value = mock_response

    result = api.fetch_data("I hate tests")
    assert result[0]["key"] == "1"


@patch("requests.get")
def test_connect_failure_500(mock_get, api):

    mock_response = requests.Response()
    mock_response.status_code = 500
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        api._connect()


@patch("requests.get")
def test_connect_failure_404(mock_get, api):
    mock_response = requests.Response()
    mock_response.status_code = 404
    mock_get.return_value = mock_response

    with pytest.raises(Exception):
        api._connect()


@patch.object(HeadHunterAPI, "_connect")
@patch("requests.get")
def test_fetch_data_with_mocked_connect(mock_get, mock_connect, capsys, api):

    mock_connect.return_value = None
    mock_get.side_effect = requests.exceptions.Timeout("Request timed out")

    vacancies = api.fetch_data("Python")
    captured = capsys.readouterr()

    assert vacancies == []
    assert "Ошибка получения данных" in captured.out
