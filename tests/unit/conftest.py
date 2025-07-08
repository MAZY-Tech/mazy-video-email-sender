import pytest

@pytest.fixture(autouse=True)
def prevent_mongo_connection(mocker):
    mocker.patch("src.database.MongoClient")