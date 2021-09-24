from django.test import SimpleTestCase
from django.urls import resolve, reverse
from imagesapp.views import UserImagesViewSet

class TestUrls(SimpleTestCase):

    def test_list_url_is_resolved(self):
        """
        testing list url method for our UserImages model
        """
        url = reverse('imagesapp:images-list')

        self.assertEquals(resolve(url).func.__name__, UserImagesViewSet.as_view({'get': 'list'}).__name__)