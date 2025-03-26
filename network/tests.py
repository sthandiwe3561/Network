from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from .models import Profile
import io
from PIL import Image

# Create your tests here.
class ProfileModelTest(TestCase):
    def setup(self):
        """Create a sample profile for testing."""
         # Create a simple image in memory
        image_file = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image.save(image_file, format="PNG")
        image_file.name = "test_image.png"
        image_file.seek(0)

        # Create the profile with the image
        self.profile = Profile.objects.create(username="sthandiwe",
                                              image=SimpleUploadedFile(image_file.name, image_file.read())
                                              ,bio="i have this in life")

    def test_profile(self):
        """Test if a profile is created with an image."""
        self.assertEqual(self.profile.username,"sthandiwe")
        self.assertTrue(self.profile.image.name.endswith('test_image.png'))
        self.assertEqual(self.profile.bio,"i have this in life")



    
    

