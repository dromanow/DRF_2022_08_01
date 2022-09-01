from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import AuthorModelViewSet, BookModelViewSet

app_name = 'library'

router = DefaultRouter()
# router = SimpleRouter()
router.register('authors', AuthorModelViewSet)
router.register('books', BookModelViewSet)

urlpatterns = [
    path('', include(router.urls))
]
