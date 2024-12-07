from django.test import TestCase
from django.contrib.auth.models import User
from .models import Post

class PostTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

    def test_model_str(self):
        # Create a Post instance with the user as the author
        obj = Post.objects.create(
            title="test post",
            author=self.user
        )
        # Verify the __str__ method of the Post model
        self.assertEqual(str(obj), "test post")
