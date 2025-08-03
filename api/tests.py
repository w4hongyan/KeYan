from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status

User = get_user_model()


class UserRegistrationTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.registration_data = {
            'username': 'testuser',
            'password': 'testpassword123',
            'email': 'test@example.com',
            'nickname': 'Test User'
        }

    def test_user_registration_success(self):
        """测试用户成功注册"""
        response = self.client.post('/api/register/', self.registration_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(User.objects.get().username, 'testuser')

    def test_user_registration_missing_fields(self):
        """测试缺少必要字段时注册失败"""
        incomplete_data = {
            'username': 'testuser',
            'email': 'test@example.com'
        }
        response = self.client.post('/api/register/', incomplete_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(User.objects.count(), 0)
