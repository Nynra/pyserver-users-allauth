from django.test import TestCase
from users.models import CustomUser


class TestCustomUser(TestCase):
    def setUp(self):
        self.data = {
            "username": "test_user",
            "nickname": "test_nickname",
            "email": "test@test.com",
            "password": "foo",
        }

    def test_attributes(self):
        """Test if the model has the correct attributes."""
        model = CustomUser.objects.create_user(**self.data)

        for key in self.data.keys():
            if key == "password":
                continue
            self.assertEqual(
                getattr(model, key),
                self.data[key],
                "Attribute {} is not correct, expected {}, got {}".format(
                    key, self.data[key], getattr(model, key)
                ),
            )

        # Validate the password
        self.assertTrue(model.check_password(self.data["password"]))
        self.assertFalse(model.check_password("bar"))

    def test_create(self):
        """Test if the model can create a new database entry."""
        search_kwargs = {"username": self.data["username"]}
        CustomUser.objects.create_user(**self.data)
        self.assertTrue(CustomUser.objects.filter(**search_kwargs).exists())

        # Check if the attributes are correct
        model = CustomUser.objects.get(**search_kwargs)
        for key in self.data.keys():
            if key == "password":
                continue
            self.assertEqual(
                getattr(model, key),
                self.data[key],
                "Attribute {} is not correct, expected {}, got {}".format(
                    key, self.data[key], getattr(model, key)
                ),
            )

        # Validate the password
        self.assertTrue(model.check_password(self.data["password"]))
        self.assertFalse(model.check_password("bar"))


class UsersManagersTests(TestCase):
    def setUp(self):
        self.data = {
            "username": "test_user",
            "nickname": "test_nickname",
            "email": "test@test.com",
            "password": "foo",
        }

    def test_create_user(self):
        # Setup
        user = CustomUser.objects.create_user(**self.data)
        user.full_clean()

        # Assert
        for key, value in self.data.items():
            # Skip the password as this is hashed
            if key == "password":
                continue
            self.assertEqual(getattr(user, key), value)

        # Validate the password
        self.assertTrue(user.check_password(self.data["password"]))

        # Missing email
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                username="test_user", password="foo", nickname="test_nickname"
            )

        # Missing username
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                email="test@test.com", password="foo", nickname="test_nickname"
            )

        # Missing nickname
        with self.assertRaises(TypeError):
            CustomUser.objects.create_user(
                username="test_user", password="foo", email="test@test.com"
            )


    def test_create_superuser(self):
        # Setup
        admin_user = CustomUser.objects.create_superuser(
            username="super_user", password="foo", nickname="test_nickname",
            email="test@test.com",
        )

        # Test setting attributes
        self.assertEqual(admin_user.username, "super_user")
        self.assertEqual(admin_user.nickname, "test_nickname")
        self.assertTrue(admin_user.is_active)
        self.assertTrue(admin_user.is_staff)
        self.assertTrue(admin_user.is_superuser)

        admin_user.full_clean()