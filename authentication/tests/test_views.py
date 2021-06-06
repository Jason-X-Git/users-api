from rest_framework import status
from django.test import TestCase, Client
from django.urls import reverse
from authentication.models import CustomUser, CustomPermission
from authentication.serializers import CustomUserSerializer, CustomPermissionSerializer
from rest_framework.test import APITestCase
import random

# initialize the APIClient app
client = Client()


class UserGetTest(APITestCase):
    """ Test module for GET all puppies API """

    def setUp(self):
        self.users = []
        self.user_number = 5
        for i in range(self.user_number):
            user = CustomUser(email='test-user-{}@msn.com'.format(i))
            user.set_password('1234qwer@')
            user.save()
            self.users.append(user)

    def test_get_all_users(self):
        """Test getting all users"""
        # get API response
        response = self.client.get(reverse('user-list'))
        # get data from db
        users = CustomUser.objects.all()
        serializer = CustomUserSerializer(users, many=True)
        self.assertEqual(users.count(), self.user_number)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_get_user_by_id(self):
        """Test getting user by id"""
        user = self.users[random.randint(0, len(self.users)-1)]
        response = self.client.get(reverse('user-detail', kwargs={'pk': user.id}))
        serializer = CustomUserSerializer(user)
        self.assertEqual(response.data, serializer.data)


class UserCreateDeleteTest(APITestCase):
    """Test creating and deleting user"""

    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(email='admin-user@gmail.com', password='1234qwer@')
        self.normal_user = CustomUser.objects.create_user(email='normal-user@hotmail.com', password='422^547ddee')

        self.new_user = {'email': 'newuser@gmail.com', 'given_name': 'Sherry', 'family_name': 'Griffin',
                         'password': '12dqq3r1fq23@'}

    def test_login_required(self):
        """Test authenticated user required"""
        response = self.client.post(reverse('user-list'), self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN, 'Should only allow for authenticated user.')

    def test_create_user_success(self):
        """Test creating user success with authenticated admin user"""
        self.client.force_authenticate(user=self.admin_user)
        response = self.client.post(reverse('user-list'), self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data.get('email'), self.new_user.get('email'))
        self.assertEqual(response.data.get('family_name'), self.new_user.get('family_name'))

    def test_create_user_failure(self):
        """Test creating user failure with authenticated non-admin user"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(reverse('user-list'), self.new_user, format='json')
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_delete_user_success(self):
        """Test creating user success with authenticated admin user"""
        self.client.force_authenticate(user=self.admin_user)
        before_count = CustomUser.objects.count()
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.normal_user.id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(CustomUser.objects.count(), before_count - 1, 'Should have one user deleted.')
        self.assertTrue(self.normal_user not in CustomUser.objects.all())

    def test_delete_user_failure(self):
        """Test creating user success with authenticated non-admin user"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(reverse('user-detail', kwargs={'pk': self.normal_user.id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class PermissionTest(APITestCase):
    def setUp(self):
        self.admin_user = CustomUser.objects.create_superuser(email='admin-user@gmail.com', password='1234qwer@')
        self.normal_user = CustomUser.objects.create_user(email='normal-user@hotmail.com', password='422^547ddee')

        new_user = {'email': 'newuser@gmail.com', 'given_name': 'Sherry',
                    'family_name': 'Griffin', 'password': '12dqq3r1fq23@'}

        self.client.force_authenticate(user=self.admin_user)
        self.client.post(reverse('user-list'), new_user, format='json')
        self.test_user = CustomUser.objects.get(email=new_user.get('email'))
        self.playload = {
            'user': self.test_user,
            'permission_type': 'Level 3',
        }

    def test_grant_permission_success(self):
        """Test granting permission success with authenticated admin user"""
        self.client.force_authenticate(user=self.admin_user)

        response = self.client.post(reverse('permission-list'), self.playload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(self.test_user.custom_permission.permission_type, self.playload.get('permission_type'))
        self.assertEqual(self.test_user.custom_permission.user, self.test_user)

    def test_grant_permission_failure(self):
        """Test granting permission failure with authenticated non-admin user"""
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.post(reverse('permission-list'), self.playload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_revoke_permission_success(self):
        """Test revoking permission success with authenticated admin user"""
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(reverse('permission-list'), self.playload)
        response = self.client.delete(reverse('permission-detail',
                                              kwargs={'pk': self.test_user.custom_permission.user_id}))
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

    def test_revoke_permission_failure(self):
        """Test revoking permission failure with authenticated non-admin user"""
        self.client.force_authenticate(user=self.admin_user)
        self.client.post(reverse('permission-list'), self.playload)
        self.client.force_authenticate(user=self.normal_user)
        response = self.client.delete(reverse('permission-detail',
                                              kwargs={'pk': self.test_user.custom_permission.user_id}))
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
