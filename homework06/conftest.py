import pytest

from mysql.client import MysqlClient


@pytest.fixture(scope='session')
def mysql_client():
    mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
    mysql_client.connect()
    yield mysql_client
    mysql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        mysql_client = MysqlClient(user='root', password='pass', db_name='TEST_SQL')
        mysql_client.recreate_db()

        mysql_client.connect()
        mysql_client.create_total_requests()
        mysql_client.create_requests_of_type()
        mysql_client.create_frequent_requests()
        mysql_client.create_big_failed_requests()
        mysql_client.create_threat_origins()

        mysql_client.connection.close()
