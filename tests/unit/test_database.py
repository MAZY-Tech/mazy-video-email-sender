import pytest
from unittest.mock import patch, MagicMock
import database

@pytest.fixture(autouse=True)
def reset_client():
    database._client = None
    yield
    database._client = None

@patch('database.DATABASE_NAME', 'test_db')
@patch('database.DATABASE_HOST', 'test_host')
@patch('database.DATABASE_PASSWORD', 'test_password')
@patch('database.DATABASE_USER', 'test_user')
@patch('database.MongoClient')
def test_get_db_collection_connects_on_first_call(mock_mongo_client):
    mock_db = MagicMock()
    mock_collection = MagicMock()
    
    mock_mongo_client.return_value.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection
    
    result_collection = database.get_db_collection()

    mock_mongo_client.assert_called_once()

    expected_uri = "mongodb+srv://test_user:test_password@test_host/?retryWrites=true&w=majority&appName=mazy-video-tools"
    mock_mongo_client.assert_called_with(expected_uri)

    mock_mongo_client.return_value.__getitem__.assert_called_with('test_db')
    mock_db.__getitem__.assert_called_with('notification_history')

    assert result_collection == mock_collection

@patch('database.DATABASE_NAME', 'test_db')
@patch('database.DATABASE_HOST', 'test_host')
@patch('database.DATABASE_PASSWORD', 'test_password')
@patch('database.DATABASE_USER', 'test_user')
@patch('database.MongoClient')
def test_get_db_collection_reuses_existing_client(mock_mongo_client):
    mock_db = MagicMock()
    mock_collection = MagicMock()
    mock_mongo_client.return_value.__getitem__.return_value = mock_db
    mock_db.__getitem__.return_value = mock_collection

    collection1 = database.get_db_collection()
    collection2 = database.get_db_collection()

    mock_mongo_client.assert_called_once()

    assert collection1 == mock_collection
    assert collection2 == mock_collection