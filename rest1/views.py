from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, at polls index")

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest1.serializers import UserSerializer, GroupSerializer
from rest1.models import Data,Snippet
from rest1.serializers import DataSerializer,SnippetSerializer
from rest_framework.pagination import LimitOffsetPagination
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import mixins
from rest_framework import generics
from rest_framework.request import Request

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    API端：允许查看和编辑用户
    """
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    """
    API端：允许查看和编辑组
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import authentication, permissions
from rest1.serializers import UserSerializer1

from rest_framework import generics
from django.contrib.auth.models import User
class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer1
    def perform_create(self,serialzer):
        serialzer.save(owner=self.request.user)

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer1


#
# class SnippetList(APIView):
#     """
#     List all snippets, or create a new snippet.
#     """
#     def get(self, request, format=None):
#         snippets = Snippet.objects.all()
#         Request.query_params
#         serializer = SnippetSerializer(snippets, many=True)
#         return Response(serializer.data)
# #
#     def post(self, request, format=None):
#         # data = JSONParser.parse(request)
#         serializer = SnippetSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
# class CustomPagination(LimitOffsetPagination):

class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
# class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    pagination_class = LimitOffsetPagination
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    # queryset = Snippet.objects.all()
    # serializer_class = SnippetSerializer
    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def get(self, request, *args, **kwargs):
    #     return self.list(request, *args, **kwargs)

    # def list(self,request,*args,**kwargs):
    #     return self.create(request,*args,**kwargs)

class SnippetDetail(APIView):
    """
    Retrieve, update or delete a snippet instance.
    """
    def get_object(self, pk):
        try:
            return Snippet.objects.get(pk=pk)
        except Snippet.DoesNotExist:
            raise Http404

    def get(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet)
        return Response(serializer.data)

    def put(self, request, pk, format=None):
        snippet = self.get_object(pk)
        serializer = SnippetSerializer(snippet, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk, format=None):
        snippet = self.get_object(pk)
        snippet.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
