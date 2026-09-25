import pytest
from apirest import MemoryStore
from api_comun import crear_api

@pytest.fixture
def client():
    return crear_api(MemoryStore()).test_client()

def test_crud(client):
    assert len(client.get('/books').json['books']) == 2
    created = client.post('/books', json={'title':'Cien años de soledad', 'author':'Gabo'})
    assert created.status_code == 201
    url = created.headers['Location']
    assert client.get(url).json['book']['title'] == 'Cien años de soledad'
    assert client.put(url, json={'author':'Gabriel García Márquez'}).json['book']['author'] == 'Gabriel García Márquez'
    assert client.delete(url).json == {'result': True}
    assert client.get(url).status_code == 404

@pytest.mark.parametrize('payload', [None, [], {}, {'title':''}, {'title':'  '}, {'title':9}, {'title':True}, {'title':'a'*256}, {'title':'A','unknown':'x'}, {'title':'A','author':None}])
def test_invalid_create(client, payload):
    assert client.post('/books', json=payload).status_code == 400

@pytest.mark.parametrize('method', ['get','put','delete'])
def test_missing(client, method):
    kwargs={'json':{'title':'Cambio'}} if method=='put' else {}
    assert getattr(client, method)('/books/999999', **kwargs).status_code == 404

def test_delete_all_and_create(client):
    client.delete('/books/1'); client.delete('/books/2')
    assert client.get('/books').json == {'books':[]}
    assert client.post('/books', json={'title':'Nuevo'}).json['book']['id'] == 3

def test_ids_not_reused(client):
    first=client.post('/books', json={'title':'A'}).json['book']['id']
    client.delete(f'/books/{first}')
    assert client.post('/books', json={'title':'B'}).json['book']['id'] > first

def test_sql_string_is_data(client):
    value="Libro'); DROP TABLE books; --"
    response=client.post('/books', json={'title':value})
    assert response.json['book']['title'] == value
    assert client.get('/books').status_code == 200

def test_memory_restart():
    first=crear_api(MemoryStore()).test_client()
    first.post('/books', json={'title':'Temporal'})
    second=crear_api(MemoryStore()).test_client()
    assert len(first.get('/books').json['books']) == 3
    assert len(second.get('/books').json['books']) == 2

def test_malformed_json(client):
    assert client.post('/books', data='{broken', content_type='application/json').status_code == 400

def test_unknown_route_json(client):
    r=client.get('/inexistente')
    assert r.status_code == 404 and r.is_json

def test_reject_empty_update(client):
    assert client.put('/books/1', json={}).status_code == 400

def test_health(client):
    assert client.get('/health').json['storage'] == 'MemoryStore'
