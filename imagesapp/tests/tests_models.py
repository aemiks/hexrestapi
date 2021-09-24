from django.test import TestCase
from imagesapp.models import User, Profile

class ProfileModelTest(TestCase):

    def setUp(self):
        self.user = User()
        self.user.username = 'Test'
        self.user.save()
        created_user = User.objects.get(pk=1)
        self.profile = Profile.objects.filter(user=created_user).get()

    def test_create_profile(self):
        """
        test if Profile is automaticly created for User
        """
        record = Profile.objects.get(pk=1)
        self.assertEqual(record, self.profile)

    def test_profile_tier(self):
        """
        checks if a basic plan is automatically added to the profile
        this test also checks if a Basic plan has been automatically created
        """
        self.assertEqual(self.profile.user_tier.name, 'Basic')

