from django.test import TestCase
from .factories import ProfileFactory, UserFactory

class AccountTestCase(TestCase):
    def setUp(self):
        self.test_user = UserFactory()        

    def test_user_is_created(self):
        """ test that the user instance is created and saved successfully"""
        self.assertTrue(self.test_user)

    def test_user_is_active(self):
        """ test that the user instance is active by default """
        self.assertTrue(self.test_user.is_active)

    def test_profile_is_created_for_user(self):
        """ test that a profile instance has been created for the saved user instance and saved """
        self.profile = self.test_user.profile
        self.assertTrue(self.profile)

    def test_user_is_not_staff(self):
        """ test that all created users are not staffs by default """
        self.assertFalse(self.test_user.is_staff)

    def test_user_cannot_be_deleted_destructively(self):
        """ test that deleted user's record are still stored in the db for retrival """
        self.test_user.delete()
        self.assertFalse(self.test_user.is_active)