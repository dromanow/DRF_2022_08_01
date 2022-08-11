import io

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import mixins
from rest_framework.response import Response
from rest_framework.decorators import api_view, renderer_classes, action
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from rest_framework.pagination import LimitOffsetPagination
from .models import Author, Book
from .serializers import AuthorModelSerializer, AuthorSerializer, BookModelSerializer, BookSerializer


class AuthorLimitOffsetPagination(LimitOffsetPagination):
    default_limit = 2


class AuthorModelViewSet(ModelViewSet):
    pagination_class = AuthorLimitOffsetPagination
    serializer_class = AuthorModelSerializer
    queryset = Author.objects.all()

    @action(detail=True, methods=['get'])
    def get_author_name(self, request, pk):
        author = get_object_or_404(Author, pk=pk)
        return Response({'name': str(author)})

    def get_queryset(self):
        first_name = self.request.query_params.get('first_name', None)
        if first_name:
            return Author.objects.filter(first_name__containt=first_name)
        return Author.objects.all()


class BookModelViewSet(ModelViewSet):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()


class BookModelLimitedViewSet(
    mixins.RetrieveModelMixin,
    mixins.ListModelMixin,
    mixins.UpdateModelMixin,
    GenericViewSet
):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()


class BookApiView(APIView):
    renderer_classes = [JSONRenderer]

    def get(self, request):
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)


class BookListAPIView(ListAPIView):
    renderer_classes = [JSONRenderer]
    serializer_class = BookSerializer
    queryset = Book.objects.all()


@api_view(['GET'])
@renderer_classes([JSONRenderer])
def book_api_get(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)
    return Response(serializer.data)


def book_get(request):
    books = Book.objects.all()
    serializer = BookSerializer(books, many=True)

    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data)


def author_get(request, pk=None):
    if pk is not None:
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author)
    else:
        authors = Author.objects.all()
        serializer = AuthorSerializer(authors, many=True)

    json_data = JSONRenderer().render(serializer.data)
    return HttpResponse(json_data)


@csrf_exempt
def author_post(request, pk=None):
    json_data = JSONParser().parse(io.BytesIO(request.body))

    if request.method == 'POST':
        serializer = AuthorSerializer(data=json_data)
    elif request.method == 'PUT':
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, data=json_data)
    elif request.method == 'PATCH':
        author = Author.objects.get(pk=pk)
        serializer = AuthorSerializer(author, data=json_data, partial=True)

    if serializer.is_valid():
        author = serializer.save()

        serializer = AuthorSerializer(author)
        json_data = JSONRenderer().render(serializer.data)
        return HttpResponse(json_data)

    return HttpResponseBadRequest(JSONRenderer().render(serializer.errors))
