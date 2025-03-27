from django.core.files.uploadedfile import SimpleUploadedFile
from django.contrib.auth import get_user_model
from django.test import TestCase, Client
from django.urls import reverse
from network.models import Profile,Post
import io
from PIL import Image

"""Tessting Profile"""
# Create your tests here.
class ProfileModelTest(TestCase):
    def setUp(self):
        """Create a sample profile model for testing."""
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

#profilefunction test case
class ProfileViewTest(TestCase):
    def setUp(self):
         #for making HTTP request to stimulate web user testing functions
        self.client = Client()
        User = get_user_model()
        self.user = User.objects.create_user(username="sthandiwe", password="password123")
        self.client.login(username="sthandiwe", password="password123")

    def test_profile_get_request(self):
        #show the profile form reverse to the profile form
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code,200)
        self.assertContains(response, '<form')

    def test_profile_post_request(self):
        """Test if a profile is created/updated correctly."""
        image_file = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image.save(image_file, format="PNG")
        image_file.name = "test_image.png"
        image_file.seek(0)

        response = self.client.post(reverse('profile'), {
            "username": "new_username",
            "description": "Updated bio",
            "image": SimpleUploadedFile(image_file.name, image_file.read()),
        })

        self.assertEqual(response.status_code, 302)  # Should redirect to index
        self.assertTrue(Profile.objects.filter(user=self.user, username="new_username").exists())
            
"""Testing Post"""
#testing post model
class PostModelTest(TestCase):

    #create a test case to test with
    def setUp(self):
        #creating a user
        User = get_user_model()
        self.user = User.objects.create_user(username="sthandiwe", password="password123")

        #create an image to put in image field for test
        image_file = io.BytesIO()
        image = Image.new("RGB", (100, 100), color=(255, 0, 0))
        image.save(image_file, format="PNG")
        image_file.name = "test_image.png"
        image_file.seek(0)

        #creating data for post fields
        self.post = Post.objects.create(user = self.user, 
                                        content = "God is all I have",
                                        image=SimpleUploadedFile(image_file.name, image_file.read())  # Add the image here
                                               )
        
    #test function
    def test_post(self):
        print(f"Image path: {self.post.image.name}")

        self.assertEqual(self.post.content, "God is all I have")
        self.assertTrue(self.post.image.name.startswith('posts/test_image'))

class PostViewTest(TestCase):
    def setUp(self):
         #for making HTTP request to stimulate web user testing functions
         self.client = Client()
         User = get_user_model()
         self.user = User.objects.create_user(username="sthandiwe", password="password123")
         self.client.login(username="sthandiwe", password="password123")
         self.post = Post.objects.create(user=self.user, content="Test Content")

    def test_create_post_get_request(self):
        """Test that the create post page returns a 200 status code."""
        response = self.client.get(reverse("create_post"))  # Assuming your URL name is 'create_post'
        self.assertEqual(response.status_code, 200)  # Check if GET request works

    def test_edit_post_get_request(self):
        """Test that the edit post page returns a 200 status code."""
        response = self.client.get(reverse("edit_post", args=[self.post.id]))  # Assuming 'edit_post' needs post_id
        self.assertEqual(response.status_code, 200)  # Check if GET request works



        

        







        



    
    

