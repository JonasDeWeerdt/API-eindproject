import requests
import json
import re


def test_create_caretaker():
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    data = {"email": "jonas.de.Weerdt@outlook.com", "password": "root"}
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://127.0.0.1:8000/caretakers/", json=data, headers=headers)
    assert response.status_code == 201
    assert bool(re.search(email_regex, json.loads(response.text)["email"])) == True
    assert type(json.loads(response.text)["id"]) == int


def test_read_caretaker():
    response = requests.get('http://127.0.0.1:8000/caretakers/2')
    assert response.status_code == 200
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    assert bool(re.search(email_regex, json.loads(response.text)["email"])) == True


def test_read_caretakers():
    response = requests.get('http://127.0.0.1:8000/caretakers/?skip=0&limit=2')
    assert response.status_code == 200
    assert json.loads(response.text)[0]["id"] == 1  # To check if the skip is not higher than zero because then the first id would be higher then 1
    assert len(json.loads(response.text)) == 2  # To check the limit
    email_regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    # for id in range(0,len(json.loads(response.text))):
    #    assert bool(re.search(email_regex, json.loads(response.text)[id]["email"])) == True


def test_read_caretaker_wrong_with_string():
    response = requests.get('http://127.0.0.1:8000/caretakers/two')
    assert response.status_code == 422


def test_create_animal_for_caretaker():
    data = {"name": "badger", "gender": "female"}
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://127.0.0.1:8000/animals/2", json=data, headers=headers)
    assert response.status_code == 201
    assert json.loads(response.text.lower())["gender"] == "male" or json.loads(response.text.lower())["gender"] == "female"
    assert json.loads(response.text)["caretaker_id"] == 2


def test_read_animals():
    response = requests.get('http://127.0.0.1:8000/animals/?skip=0&limit=2')
    assert response.status_code == 200
    assert json.loads(response.text)[0]["id"] == 1  # To check if the skip is not higher than zero because then the first id would be higher then 1
    assert len(json.loads(response.text)) == 2  # To check the limit
    for id in range(0, len(json.loads(response.text))):
        assert json.loads(response.text.lower())["gender"] == "male" or json.loads(response.text.lower())["gender"] == "female"


def test_read_animal():
    response = requests.get('http://127.0.0.1:8000/animals/1')
    assert response.status_code == 200
    assert json.loads(response.text.lower())["gender"] == "male" or json.loads(response.text.lower())["gender"] == "female"


def test_create_toy_for_animal():
    data = {"title": "rope", "description": "1 Meter long rope"}
    headers = {"Content-Type": "application/json"}
    response = requests.post("http://127.0.0.1:8000/toys/2", json=data, headers=headers)
    assert response.status_code == 201
    assert json.loads(response.text)["owner_id"] == 2


def test_read_toys():
    response = requests.get('http://127.0.0.1:8000/toys/?skip=1&limit=2')
    assert response.status_code == 200
    assert json.loads(response.text)[0]["id"] == 2  # To check if the skip is not higher than zero because then the first id would be higher then 1
    assert len(json.loads(response.text)) == 1  # To check the limit

