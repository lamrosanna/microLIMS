from django.test import TestCase
from django.contrib.auth import get_user_model
from customers.models import company


class UsersManagersTest(TestCase):
    def setUp(self) -> None:
        customer = company.objects.create(
        company_name="Test Company 1",
        customer_contact="Test Contact 1", 
        address="Test Address 123", 
        city="Test",
        state="CO", 
        phone="999999999",
        entity="CUSTOMER")
        customer.save()
    def test_create_user(self):
        User = get_user_model()
        testcompany = company.objects.get(company_name="Test Company 1")
        user = User.objects.create_user(email="normal@user.com", password="foo", company_id=testcompany.id)
        self.assertEqual(user.email, "normal@user.com")
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(user.username)
        except AttributeError:
            pass
        with self.assertRaises(TypeError):
            User.objects.create_user()
        with self.assertRaises(TypeError):
            User.objects.create_user(email="")
        with self.assertRaises(ValueError):
            User.objects.create_user(email="", password="foo")

    def test_create_superuser(self):
        User = get_user_model()
        testcompany = company.objects.get(company_name="Test Company 1")
        admin_user = User.objects.create_superuser(email="super@user.com", password="foo",company_id=testcompany.id)
        self.assertEqual(admin_user.email, "super@user.com")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)
        try:
            # username is None for the AbstractUser option
            # username does not exist for the AbstractBaseUser option
            self.assertIsNone(admin_user.username)
        except AttributeError:
            pass
        with self.assertRaises(ValueError):
            User.objects.create_superuser(
                email="super@user.com", password="foo", is_superuser=False)