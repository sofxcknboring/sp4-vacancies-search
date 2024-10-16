import pytest
from unittest.mock import patch, Mock
from src.headhunter_api import HeadHunterAPI

@pytest.fixture
def api():
    return HeadHunterAPI()

@patch.object(HeadHunterAPI, 'connect', return_value=True)
@patch('requests.get')
def test_fetch_data_success(mock_get, mock_connect, api):

    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.json.return_value = {'items': ['some_data1', 'some_data2']}
    mock_get.return_value = mock_response

    result = api.fetch_data('some_keyword')

    assert result == ['some_data1', 'some_data2']

    mock_connect.assert_called_once()
