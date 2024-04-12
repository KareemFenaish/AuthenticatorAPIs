from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User, UserDetails

'''
To migrate:
python manage.py makemigrations
python manage.py migrate

To run server: python manage.py runserver

To run tests: python manage.py test

Ctrl+C to break
'''

class UserAPITests(APITestCase):
    def setUp(self):
        # Create a user for testing login
        self.user_data = {
            'first_name': 'John',
            'last_name': 'Doe',
            'email': 'john.doe@example.com',
            'phone': '9876543210',
            'password': 'mypassword'
        }
        self.user = User.objects.create_user(**self.user_data)
        self.user.set_password(self.user_data['password'])
        self.user.save()

        # Create user details for the user
        UserDetails.objects.create(
            user=self.user,
            age=25,
            dob='1999-01-01',
            profession='Engineer',
            address='123 Main St',
            hobby='Reading'
        )

        # Get JWT tokens for the user
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)


    def test_signup_api(self):
        url = reverse('signup')
        data = {
            'first_name': 'Jane',
            'last_name': 'Smith',
            'email': 'jane.smith@example.com',
            'phone': '1234567890',
            'password': 'password123'
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_login_api(self):
        url = reverse('login')
        data = {
            'email': self.user_data['email'],
            'password': self.user_data['password']
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('access', response.data)

    def test_add_user_details_api(self):
        url = reverse('add_user_details')
        data = {
            'age': 30,
            'dob': '1990-01-01',
            'profession': 'Engineer',
            'address': '123 Main St',
            'hobby': 'Reading'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_update_user_profile_api(self):
        url = reverse('update_user_profile')
        data = {
            'profession': 'Senior Engineer',
            'address': '456 Elm St',
            'hobby': 'Hiking'
        }
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.put(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_delete_user_api(self):
        url = reverse('delete_user')
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
