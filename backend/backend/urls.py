"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter, SimpleRouter
from library.views import *

router = DefaultRouter()
# router = SimpleRouter()
router.register('authors', AuthorModelViewSet)
# router.register('books', BookModelViewSet)
router.register('books', BookModelLimitedViewSet)

# http://127.0.0.1:8002/api/authors/?first_name=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('author_get', author_get),
    path('book_get', book_get),
    path('book_api_get', book_api_get),
    path('book_api_get_class', BookApiView.as_view()),
    path('book_api_get_list', BookListAPIView.as_view()),
    path('book_api_view_set', BookModelLimitedViewSet.as_view({'get': 'list'})),
    path('book_api_view_set/<int:pk>', BookModelLimitedViewSet.as_view({'get': 'retrieve'})),
    path('author_api_view_set/kwargs/<str:first_name>', AuthorModelViewSet.as_view({'get': 'list'})),
    path('author_get/<int:pk>', author_get),
    path('author_post', author_post),
    path('author_post/<int:pk>', author_post),
]
