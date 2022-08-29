import random

from django.contrib.auth.models import User
from django.test import TestCase
from rest_framework import status
from rest_framework.test import APIRequestFactory, force_authenticate, APIClient, APITestCase
from mixer.backend.django import mixer

from .models import Author, Bio
from .views import AuthorModelViewSet


class AuthorTestCase(TestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username='denis', password='qwerty')
        self.author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)

    def test_get_list(self):
        factory = APIRequestFactory()
        request = factory.get('/api/authors/')
        view = AuthorModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_1(self):
        factory = APIRequestFactory()
        request = factory.get('/api/authors/')
        force_authenticate(request, user=self.user)
        view = AuthorModelViewSet.as_view({'get': 'list'})
        response = view(request)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)


class AuthorClientTestCase(APITestCase):

    def setUp(self) -> None:
        self.user = User.objects.create_superuser(username='denis', password='qwerty')
        # self.author = Author.objects.create(first_name='Александр', last_name='Пушкин', birthday_year=1799)
        self.author = mixer.blend(Author, birthday_year=mixer.sequence(lambda c: int(random.random()*2000)))
        self.bio = mixer.blend(Bio, author__birthday_year=1900)

    def test_get_list(self):
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_get_list_1(self):
        self.client.force_authenticate(self.user)
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_get_list_2(self):
        self.client.login(username='denis', password='qwerty')
        # self.client.force_login(user=self.user)
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.client.logout()
        response = self.client.get('/api/authors/')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post(self):
        self.client.login(username='denis', password='qwerty')
        # self.client.force_login(user=self.user)
        response = self.client.post('/api/authors/', {
            "first_name": "Федор",
            "last_name": "Достоевский",
            "birthday_year": 1820
        })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        author = Author.objects.get(pk=response.data.get('id'))
        self.assertEqual(author.last_name, 'Достоевский')

