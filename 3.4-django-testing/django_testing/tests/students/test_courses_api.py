import pytest
from rest_framework import status
from students.models import Course, Student

@pytest.mark.django_db
def test_get_first_course(api_client, course_factory):
    # Arrange
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()['id'] == course.id

@pytest.mark.django_db
def test_get_courses_list(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    url = '/api/v1/courses/'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) == 5

@pytest.mark.django_db
def test_course_filter_by_id(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    url = f'/api/v1/courses/?id={courses[0].id}'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['id'] == courses[0].id

@pytest.mark.django_db
def test_course_filter_by_name(api_client, course_factory):
    # Arrange
    courses = course_factory(_quantity=5)
    url = f'/api/v1/courses/?name={courses[0].name}'

    # Act
    response = api_client.get(url)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0]['name'] == courses[0].name

@pytest.mark.django_db
def test_create_course(api_client):
    # Arrange
    url = '/api/v1/courses/'
    data = {'name': 'New Course'}

    # Act
    response = api_client.post(url, data=data)

    # Assert
    assert response.status_code == status.HTTP_201_CREATED
    assert Course.objects.count() == 1

@pytest.mark.django_db
def test_update_course(api_client, course_factory):
    # Arrange
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'
    data = {'name': 'Updated Course'}

    # Act
    response = api_client.patch(url, data=data)

    # Assert
    assert response.status_code == status.HTTP_200_OK
    course.refresh_from_db()
    assert course.name == 'Updated Course'

@pytest.mark.django_db
def test_delete_course(api_client, course_factory):
    # Arrange
    course = course_factory()
    url = f'/api/v1/courses/{course.id}/'

    # Act
    response = api_client.delete(url)

    # Assert
    assert response.status_code == status.HTTP_204_NO_CONTENT
    assert Course.objects.count() == 0
