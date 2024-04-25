from django.contrib.auth.models import User
from django.test import TestCase
from blogposts.models import BlogPost


class BlogPostViewSetTestCase(TestCase):

    def test_no_blogs__200_and_no_contents(self):
        response = self.client.get("/blogposts/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, [])

    def test_1_blogpost__200_and_contents(self):
        # First set up data
        user = User.objects.create_user(username="testuser", password="12345")
        blogpost = BlogPost(author=user, title="Fake Title", content="Fake contents")
        blogpost.save()

        # login as the user
        self.client.force_login(user)

        # send request and see contents
        response = self.client.get("/blogposts/")
        self.assertEqual(response.status_code, 200)
        expected_data = {
            "id": blogpost.pk,
            "title": "Fake Title",
            "content": "Fake contents",
            "author": user.pk,
        }
        first_entry = response.data[0]
        for key, value in expected_data.items():
            self.assertEqual(value, first_entry[key])
