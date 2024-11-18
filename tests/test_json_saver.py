from unittest.mock import mock_open, patch


def test_get_data_empty_file(json_saver):
    with patch("builtins.open", mock_open(read_data="[]")):
        data = json_saver.get_data()
        assert data == []


def test_get_data_non_empty_file(json_saver):
    mock_data = '[{"name": "name", "url": "url", "salary": 1000, "requirement": "requirement"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        data = json_saver.get_data()
        assert data == [{"name": "name", "url": "url", "salary": 1000, "requirement": "requirement"}]


def test_get_data_invalid_json(json_saver):
    with patch("builtins.open", mock_open(read_data="{invalid_json}")):
        with patch("builtins.print") as mock_print:
            data = json_saver.get_data()
            assert data == []
            mock_print.assert_called_once_with("Ошибка декодирования JSON. Файл может быть поврежден.")


def test_add_data_new_vacancy(json_saver, vacancy1):
    with patch("builtins.open", mock_open(read_data="[]")):
        with patch("json.dump") as mock_dump:
            json_saver.add_data(vacancy1)
            mock_dump.assert_called_once()
            args, kwargs = mock_dump.call_args[0]
            assert args[0] == {
                "name": "name1",
                "employer": 1,
                "url": "url1",
                "salary": 1000,
                "requirement": "requirement1",
            }


def test_delete_data_existing_vacancy(json_saver, vacancy1):
    mock_data = '[{"name": "name1", "employer": 1, "url": "url1", "salary": 1000, "requirement": "requirement1"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("json.dump") as mock_dump:
            json_saver.delete_data(vacancy1)
            mock_dump.assert_called_once()
            args, kwargs = mock_dump.call_args[0]
            assert args == []


def test_delete_data_non_existing_vacancy(json_saver, vacancy1):
    mock_data = '[{"name": "123", "url": "123", "salary": 123, "requirement": "123"}]'
    with patch("builtins.open", mock_open(read_data=mock_data)):
        with patch("builtins.print") as mock_print:
            json_saver.delete_data(vacancy1)
            mock_print.assert_called_once_with("Вакансия не найдена")


def test_get_data_json_decode_error(json_saver, capsys):
    with patch("builtins.open", mock_open(read_data="invalid json")):
        result = json_saver.get_data()
        captured = capsys.readouterr()

        assert "Ошибка декодирования JSON. Файл может быть поврежден." in captured.out
        assert result == []
