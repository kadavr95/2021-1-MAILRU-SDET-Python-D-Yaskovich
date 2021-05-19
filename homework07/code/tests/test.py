import requests

import settings
from mock.flask_mock import SURNAME_DATA

url = f'http://{settings.APP_HOST}:{settings.APP_PORT}'


def test_add_get_user():
    resp = requests.post(f'{url}/add_user', json={'name': 'Ilya'})
    user_id_from_add = resp.json()['user_id']

    resp = requests.get(f'{url}/get_user/Ilya')
    user_id_from_get = resp.json()['user_id']

    assert user_id_from_add == user_id_from_get


def test_get_non_existent_user():
    resp = requests.get(f'{url}/get_user/dnsfndksfnkjsdnfjkdsjkfnsd')
    assert resp.status_code == 404


def test_add_existent_user():
    requests.post(f'{url}/add_user', json={'name': 'Ilya1'})
    resp = requests.post(f'{url}/add_user', json={'name': 'Ilya1'})
    assert resp.status_code == 400


def test_get_age():
    requests.post(f'{url}/add_user', json={'name': 'Vasya'})

    resp = requests.get(f'{url}/get_user/Vasya')

    assert isinstance(resp.json()['age'], int)
    assert 0 <= resp.json()['age'] <= 100

    print(resp.json()['age'])


def test_has_surname():
    SURNAME_DATA['Olya'] = 'Zaitceva'

    requests.post(f'{url}/add_user', json={'name': 'Olya'})

    resp = requests.get(f'{url}/get_user/Olya')
    assert resp.json()['surname'] == 'Zaitceva'

    print(resp.json())


def test_has_not_surname():
    requests.post(f'{url}/add_user', json={'name': 'Sveta'})

    resp = requests.get(f'{url}/get_user/Sveta')
    assert resp.json()['surname'] == None

    print(resp.json())


def test_by_socket():
    requests.post(f'{url}/add_user', json={'name': 'Egor'})

    import socket
    import json

    host = settings.APP_HOST
    port = int(settings.APP_PORT)

    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    client.settimeout(0.1)

    client.connect((host, port))

    params = '/get_user/Egor'
    request = f'GET {params} HTTP/1.1\r\nHost:{host}\r\n\r\n'

    client.send(request.encode())

    total_data = []

    while True:
        data = client.recv(4096)
        if data:
            total_data.append(data.decode())
        else:
            client.close()
            break

    data = ''.join(total_data).splitlines()

    print(data)

    assert json.loads(data[-1])['age'] > 0
