from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse

from blogposts.models import BlogPost


class BlogPostViewSetTestCase(TestCase):
    """First we test hitting the multiple endpoint for a list of blog posts, and creating a blog post"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_get_list__no_blogposts__200_and_no_contents(self):
        response = self.client.get(reverse("plural"))

        # prove auth is necessary
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.get(reverse("plural"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        self.assertEqual(response.data, [])

    def test_get_list__1_blogpost__200_and_contents(self):
        # First set up data
        blogpost = BlogPost(
            author=self.user, title="Fake Title", content="Fake contents"
        )
        blogpost.save()

        # prove auth is necessary
        response = self.client.get(reverse("plural"))
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.get(reverse("plural"))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, list)
        expected_data = {
            "id": blogpost.pk,
            "title": "Fake Title",
            "content": "Fake contents",
            "author": self.user.pk,
        }
        first_entry = response.data[0]
        for key, value in expected_data.items():
            self.assertEqual(value, first_entry[key])

    def test_post__good_data__201_object_created(self):
        """Test posting a properly formatted object results in a successful save"""
        data = {
            "title": "Fake Title",
            "content": "Fake contents",
            "author": self.user.pk,
        }

        # prove auth is necessary
        response = self.client.post(
            reverse("plural"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.post(
            reverse("plural"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 201)
        self.assertTrue(BlogPost.objects.filter(title="Fake Title").exists())

    def test_post__bad_data__400_bad_request(self):
        data = {
            "title": "Fake Title",
            "contents": "Fake contents",  # bad kwarg. Supposed to be content
            "author": self.user.pk,
        }
        # prove auth is necessary
        response = self.client.post(
            reverse("plural"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.post(
            reverse("plural"), data=data, content_type="application/json"
        )
        self.assertEqual(response.status_code, 400)


class BlogPostsViewSetSingularTestCase(TestCase):
    """in this view set, we're hitting the singular endpoint"""

    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="12345")

    def test_get_singular__no_blogposts__404(self):
        # prove auth is necessary
        response = self.client.get(reverse("singular", args=(1,)))
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.get(reverse("singular", args=(1,)))
        self.assertEqual(response.status_code, 404)

    def test_get_singular__blogpost_exists__200(self):
        blogpost = BlogPost(
            author=self.user, title="Fake Title", content="Fake contents"
        )
        blogpost.save()

        # prove auth is necessary
        response = self.client.get(reverse("singular", args=(blogpost.pk,)))
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.get(reverse("singular", args=(blogpost.pk,)))
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertEqual(response.data["title"], blogpost.title)

        # Also prove it's not a false positive
        #  0 can't be a PK
        response = self.client.get(reverse("singular", args=(0,)))
        self.assertEqual(response.status_code, 404)

    def test_put_singular__blogpost_exists_200(self):
        blogpost = BlogPost(
            author=self.user, title="Fake Title", content="Fake contents"
        )
        blogpost.save()

        data = {"title": "New Title"}
        # prove auth is necessary
        response = self.client.put(
            reverse("singular", args=(blogpost.pk,)),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.put(
            reverse("singular", args=(blogpost.pk,)),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.data, dict)
        self.assertNotEqual(response.data["title"], blogpost.title)
        self.assertEqual(response.data["title"], "New Title")

    def test_put_singular__blogpost_does_not_exist_404(self):
        self.assertEqual(0, BlogPost.objects.all().count())
        data = {"title": "New Title"}

        # prove auth is necessary
        response = self.client.put(
            reverse("singular", args=(3,)),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.put(
            reverse("singular", args=(3,)),
            data=data,
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)

    def test_delete_singular__blogpost_exists_204(self):
        blogpost = BlogPost(
            author=self.user, title="Fake Title", content="Fake contents"
        )
        blogpost.save()
        # prove auth is necessary
        response = self.client.delete(reverse("singular", args=(blogpost.pk,)))
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.delete(reverse("singular", args=(blogpost.pk,)))
        self.assertEqual(response.status_code, 204)

        self.assertEqual(0, BlogPost.objects.all().count())

    def test_delete_singular__blogpost_does_not_exist_404(self):
        # no blogpost created beforehand
        self.assertEqual(0, BlogPost.objects.all().count())
        # prove auth is necessary
        response = self.client.delete(reverse("singular", args=(3,)))
        self.assertEqual(response.status_code, 403)
        self.client.force_login(self.user)

        # now authenticated
        response = self.client.delete(reverse("singular", args=(3,)))
        self.assertEqual(response.status_code, 404)
