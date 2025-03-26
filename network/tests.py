from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase
from network.models import Profile
import io
from PIL import Image

# Create your tests here.
class ProfileModelTest(TestCase):
    def setUp(self):
        """Create a sample profile for testing."""
         # Create a user/ecause of the user foreign field in profile
        User = get_user_model()
        self.user = User.objects.create_user(username="sthandiwe", password="password123")

         # Create a simple image in memory
        image_file = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image.save(image_file, format="PNG")
        image_file.name = "test_image.png"
        image_file.seek(0)

        # Create the profile with the image
        self.profile = Profile.objects.create(
            user=self.user,  # Assign the created user to the profile
            username="sthandiwe",
            bio="I have this in life",
            image=SimpleUploadedFile(image_file.name, image_file.read())  # Add the image here
            )



    def test_profile(self):
        """Test if a profile is created with an image."""
        print(f"Image path: {self.profile.image.name}")

        self.assertEqual(self.profile.username, "sthandiwe")
        self.assertTrue(self.profile.image.name.startswith('uploads/test_image'))
        self.assertEqual(self.profile.bio, "I have this in life")

        



    
    

