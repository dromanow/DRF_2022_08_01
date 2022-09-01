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
from django.urls import path, include, re_path
from rest_framework.routers import DefaultRouter, SimpleRouter
from rest_framework.authtoken import views
from library.views import *
from drf_yasg.views import get_schema_view
from drf_yasg.openapi import Info, License, Contact

schema_view = get_schema_view(
    Info(
        title='Library',
        default_version='1.0',
        description='description',
        license=License(name='MIT'),
        contact=Contact(email='test@yandex.ru')
    )
)


# router = DefaultRouter()
# router = SimpleRouter()
# router.register('authors', AuthorModelViewSet)
# router.register('books', BookModelViewSet)
# router.register('books', BookModelLimitedViewSet)

# http://127.0.0.1:8002/api/authors/?first_name=%D0%90%D0%BB%D0%B5%D0%BA%D1%81%D0%B0%D0%BD%D0%B4%D1%80

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('library.urls')),
    # path('api/2.0/', include('library.urls', namespace='2.0')),
    # path('api/two/', include('library.urls', namespace='2.0')),
    # path('api/3.0/', include('library.urls', namespace='1.0')),
    path('api-auth/', include('rest_framework.urls')),
    path('api-auth-token/', views.obtain_auth_token),
    # path('api/<str:version>/authors', AuthorModelViewSet.as_view({'get': 'list'})),
    # re_path(r'api/(?P<version>\d.\d)/authors', AuthorModelViewSet.as_view({'get': 'list'})),
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
    path('swagger', schema_view.with_ui()),
    re_path(r'swagger(?P<format>\.json|\.yaml)', schema_view.without_ui()),
]
