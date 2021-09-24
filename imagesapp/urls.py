from django.urls import include, path
from rest_framework import routers
from imagesapp.views import UserImagesViewSet
from django.conf import settings
from django.conf.urls.static import static

app_name = 'imagesapp'

router = routers.DefaultRouter()
router.register(r'images', UserImagesViewSet, basename='images')

urlpatterns = [
    path('', include(router.urls)),

]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


