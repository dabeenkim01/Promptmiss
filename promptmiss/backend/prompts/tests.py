from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase, APIClient
from django.urls import reverse

from .models import Prompt


class PromptInteractionTests(APITestCase):
    """Tests for like and bookmark toggle endpoints."""

    def setUp(self):
        User = get_user_model()
        self.user = User.objects.create_user(username="tester", password="pass")
        self.prompt = Prompt.objects.create(user=self.user, title="t", content="c")

        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

    def test_toggle_like(self):
        url = reverse("toggle-like", args=[self.prompt.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"is_liked": True, "like_count": 1})
        self.assertEqual(self.prompt.prompt_likes.count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"is_liked": False, "like_count": 0})
        self.assertEqual(self.prompt.prompt_likes.count(), 0)

    def test_toggle_bookmark(self):
        url = reverse("toggle-bookmark", args=[self.prompt.id])

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"is_bookmarked": True, "bookmark_count": 1})
        self.assertEqual(self.prompt.bookmarks.count(), 1)

        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json(), {"is_bookmarked": False, "bookmark_count": 0})
        self.assertEqual(self.prompt.bookmarks.count(), 0)
