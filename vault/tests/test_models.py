from django.test import TestCase
from faker import Factory

from vault.models import *

faker = Factory.create()


class UserModelTest(TestCase):
    def setUp(self):
        self.obj = User.objects.create(email=faker.email())

    def test_user_creation(self):
        self.assertTrue(isinstance(self.obj, User))
        self.assertEqual(self.obj.__str__(), self.obj.__str__())


class UserManagerTest(TestCase):
    def setUp(self):
        self.user_obj_with_email = User.objects.create_user(email=faker.email())
        self.superuser_obj = User.objects.create_superuser(email=faker.email(), password=faker.random_number)

    def test_create_user_without_email(self):
        self.assertRaises(ValueError, User.objects.create_user, email='')

    def test_create_user_with_email(self):
        self.assertTrue(isinstance(self.user_obj_with_email, User))

    def test_create_superuser_with_is_staff_false(self):
        self.assertRaises(ValueError, User.objects.create_superuser, email=faker.email(), password=faker.random_number,
                          is_staff=False)

    def test_create_superuser_with_is_superuser_false(self):
        self.assertRaises(ValueError, User.objects.create_superuser, email=faker.email(), password=faker.random_number,
                          is_superuser=False)

    def test_create_superuser(self):
        self.assertTrue(isinstance(self.superuser_obj, User))


class CredentialModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(email=faker.email())
        self.obj = Credential.objects.create(owner=user, name=faker.name(), username=faker.name(),
                                             password=faker.random_number)
        self.obj.save()

    def test_secure_note_creation(self):
        self.assertTrue(isinstance(self.obj, Credential))
        self.assertEqual(self.obj.__str__(), self.obj.name)


class SecureNoteModelTest(TestCase):
    def setUp(self):
        user = User.objects.create(email=faker.email())
        self.obj = SecureNote.objects.create(owner=user, title=faker.name(), note=faker.text())
        self.obj.save()

    def test_secure_note_creation(self):
        self.assertTrue(isinstance(self.obj, SecureNote))
        self.assertEqual(self.obj.__str__(), self.obj.title)
