from django.test import TestCase
from .factories import UserFactory


class AccountTestCase(TestCase):
    """TestCases generic to the account application"""
    def setUp(self):
        self.user = UserFactory.create()        

    def test_user_is_created(self):
        """ test that the user instance is created and is successfully"""
        self.assertTrue(self.user)

    def test_user_is_active(self):
        """ test that the user instance is active by default """
        self.assertTrue(self.user.is_active)

    def test_profile_is_created_for_user(self):
        """ test that a profile instance has been created for the saved user instance and saved """
        profile = self.user.profile
        self.assertTrue(self.profile)
        self.assertTrue(profile.user is self.user)

    def test_default_user_is_not_staff(self):
        """ test that all created users are not staffs by default """
        self.assertFalse(self.user.is_staff)

    def test_user_cannot_be_deleted_destructively(self):
        """ test that deleted user's record are still stored in the db for retrival """
        self.user.delete()
        self.assertFalse(self.user.is_active)

    