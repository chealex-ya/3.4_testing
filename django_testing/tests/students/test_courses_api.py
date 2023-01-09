import pytest
from rest_framework.test import APIClient
from model_bakery import baker
from students.models import Student, Course
import random as rand


# python3 -m pytest

@pytest.fixture
def client():
    return APIClient()

@pytest.fixture
def course_factory(*args, **kwargs):
    def factory(*args, **kwargs):
        return baker.make(Course, *args, **kwargs)
    return factory

@pytest.mark.django_db
def test_1_get_course(client, course_factory):

    # count = Course.objects.count()
    courses = course_factory(_quantity = 10)

    x = rand.randrange(2, 11)

    response = client.get(f"/api/v1/courses/{x}/")

    assert response.status_code == 200

    data = response.json()
    assert x == data['id']


@pytest.mark.django_db
def test_2_list_course(client, course_factory):

    x = rand.randrange(2, 11)
    courses = course_factory(_quantity = x)
    response = client.get(f"/api/v1/courses/")

    assert response.status_code == 200

    data = response.json()
    assert len(data) == len(courses)
    for i, c in enumerate(data):
        assert c['id'] == courses[i].id


@pytest.mark.django_db
def test_3_filter_1_course(client, course_factory):

    x = rand.randrange(2, 10)
    courses = course_factory(_quantity = 10)

    id = courses[x].id

    response = client.get(f"/api/v1/courses/?id={id}")

    # assert response.status_code == 200

    data = response.json()
    assert id == data[0]['id']


@pytest.mark.django_db
def test_4_filter_1_course(client, course_factory):

    courses = course_factory(_quantity = 10)

    x = rand.randrange(1, 10)

    name = courses[x].name
    response = client.get(f"/api/v1/courses/?name={name}")

    assert response.status_code == 200

    data = response.json()
    assert name == data[0]['name']


@pytest.mark.django_db
def test_5_create_one_course(client):

    count = Course.objects.count()
    response = client.post("/api/v1/courses/", data={'name' : 'test'})

    assert response.status_code == 201
    assert Course.objects.count() == count + 1

@pytest.mark.django_db
def test_6_update_1_course(client, course_factory):

    courses = course_factory(_quantity = 10)

    x = rand.randrange(1, 10)

    id = courses[x].id
    response = client.put(f"/api/v1/courses/{id}/", data={'name': 'test'})

    assert response.status_code == 200

    data = response.json()
    assert data['name'] == 'test'

@pytest.mark.django_db
def test_7_delete_1_course(client, course_factory):

    courses = course_factory(_quantity = 10)

    x = rand.randrange(1, 10)

    id = courses[x].id
    response = client.delete(f"/api/v1/courses/{id}/")

    assert response.status_code == 204
