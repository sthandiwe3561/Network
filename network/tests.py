from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse
from .models import ProfileSetup, User
from django.core.files.uploadedfile import SimpleUploadedFile
from io import BytesIO
from PIL import Image


User = get_user_model()  # Get the active user model

class ProfileSetupTestCase(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.profile = ProfileSetup.objects.create(user=self.user)

    def test_profile_creation(self):
        """Test if profile is correctly linked to user"""
        self.assertEqual(self.profile.user.username, "testuser")
    
    def test_profile_setup(self):
        """Test if profile data is correctly fetched and saved."""


        # Create a mock image in memory
        image_file = BytesIO()
        image = Image.new('RGB', (100, 100), color = 'blue')
        image.save(image_file, 'JPEG')
        image_file.seek(0)  # Rewind the file pointer to the beginning of the file
        
         # Log in the test user
        self.client.login(username="testuser", password="password123")

        # Simulate a profile setup form submission
        response = self.client.post(reverse('profile_setup'), {
                'first_name': 'John',
                'last_name': 'Doe',
                'bio': 'This is a test bio.',
                'date_of_birth': '1990-01-01',  # <-- Testing date_of_birth
                'location': 'New York',
                'email': 'john@example.com',
                'profile_picture': SimpleUploadedFile('test_image.jpg', image_file.read(), content_type='image/jpeg')
            })
        
        # Check that the response is a redirect to the home page (or another expected view)
        self.assertEqual(response.status_code, 302)  # assuming a redirect occurs after profile setup
        
        # Fetch the updated profile from the database
        profile = ProfileSetup.objects.get(user=self.user)

        # Test if the data was correctly saved in the Profile model
        self.assertEqual(profile.user.first_name, 'John')
        self.assertEqual(profile.user.last_name, 'Doe')
        self.assertEqual(profile.bio, 'This is a test bio.')
        self.assertEqual(profile.location, 'New York')
        self.assertEqual(str(profile.birth_date), '1990-01-01')
        self.assertEqual(profile.user.email, 'john@example.com')
        
        # Test if the profile picture was saved correctly
        self.assertTrue(profile.profile_picture.name.startswith('profile_pics/'))
