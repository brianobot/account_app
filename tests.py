from django.test import TestCase
from account_app.factories import ProfileFactory, UserFactory

class AccountTestCase(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.test_profile = ProfileFactory()
        self.profile = self.user.profile

    def test_user_is_created(self):
        self.assertTrue(self.user)

    def test_profile_is_created_for_user(self):
        self.assertTrue(self.profile)