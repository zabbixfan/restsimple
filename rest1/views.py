from django.shortcuts import render
from django.http import HttpResponse
import json

def index(request):
    return HttpResponse("Hello, at polls index")

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest1.serializers import UserSerializer, GroupSerializer
from rest1.models import Data
from rest1.serializers import DataSerializer,SimpleSerializer
from rest_framework.pagination import LimitOffsetPagination


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

from rest1.models import Snippet
from rest1.serializers import SnippetSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import JSONParser
from rest_framework import mixins
from rest_framework import generics
from rest_framework.request import Request
from rest_framework.permissions import IsAuthenticated,BasePermission
from rest_framework import exceptions
from rest_framework.authentication import BaseAuthentication
import django_filters.rest_framework

class UserAuthView(BaseAuthentication):
    def authenticate(self, request):
        tk = request.query_params.get("tk")
        if tk:
            if tk == "songcheng":
                request.user = "songcheng"
                return (tk,None)
            raise exceptions.PermissionDenied("用户无权限")
        raise exceptions.AuthenticationFailed("用户认证失败")
    def authenticate_header(self, request):
        pass
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

class CustomPermisson(BasePermission):
    message = 'Adding customers not allowed.'
    # def __init__(self):
    #     self.message = 'Adding customers not allowed.'
    def has_permission(self, request, view):
        if "user" in request.query_params:
            if request.query_params['user'] == "songcheng":
                return True
        else:
            return False
class SnippetList(mixins.ListModelMixin,
                  mixins.CreateModelMixin,
                  generics.GenericAPIView):
# class SnippetList(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Snippet.objects.all()
    serializer_class = SnippetSerializer
    pagination_class = LimitOffsetPagination
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filter_backends = (django_filters.rest_framework)
    filter_fields = ('code',)
    # permission_classes = (CustomPermisson,)
    # authentication_classes = [UserAuthView,]
    def get(self, request, *args, **kwargs):
        print(request.user,'----------')
        # if request.user != 'songcheng':
        #     raise exceptions.AuthenticationFailed("yonghu cuowu")
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
        # serializer = SnippetSerializer(snippet)
        data ={

        }
        for k,v in snippet.__dict__.items():
            if not k.startswith("_"):
                data[k]=v
        print(data)
        return Response(data)

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

from django.http import QueryDict
def get_parameter_dic(request, *args, **kwargs):
    if isinstance(request, Request) == False:
        return {}

    query_params = request.query_params
    if isinstance(query_params, QueryDict):
        query_params  = {k: v for k, v in query_params.lists()}
    result_data = request.data
    if isinstance(result_data, QueryDict):
        result_data = result_data.dict()

    if query_params != {}:
        return query_params
    else:
        return result_data
class SimpleView(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    def get(self,request):
        q=Data.objects.all()
        request_data = get_parameter_dic(request)
        print(request_data)
        serializer = SimpleSerializer(data=request_data,context={'request':request})
        serializer.is_valid()
        print(json.dumps(serializer.errors))
        return Response(serializer.data)
    def post(self,request):
        request_data = get_parameter_dic(request)
        serializer = SimpleSerializer(data=request_data,context={'request':request})
        serializer.is_valid()
        return Response(serializer.data)
