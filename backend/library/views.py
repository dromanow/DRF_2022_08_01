import io

from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
from rest_framework.viewsets import ModelViewSet
from rest_framework.renderers import JSONRenderer, BrowsableAPIRenderer
from rest_framework.parsers import JSONParser
from .models import Author, Book
from .serializers import AuthorModelSerializer, AuthorSerializer, BookModelSerializer, BookSerializer


class AuthorModelViewSet(ModelViewSet):
    # renderer_classes = [JSONRenderer, BrowsableAPIRenderer]
    serializer_class = AuthorModelSerializer
    queryset = Author.objects.all()


class BookModelViewSet(ModelViewSet):
    serializer_class = BookModelSerializer
    queryset = Book.objects.all()


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
