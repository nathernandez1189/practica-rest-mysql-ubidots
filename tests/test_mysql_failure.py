from unittest.mock import patch
import pymysql
from apirest_mysql import app


def test_database_unavailable_returns_503_without_details():
    with patch('apirest_mysql.MySQLStore.connect', side_effect=pymysql.OperationalError('private database detail')):
        response=app.test_client().get('/books')
    assert response.status_code==503
    assert response.json=={'error':'Base de datos no disponible'}
    assert b'private database detail' not in response.data
