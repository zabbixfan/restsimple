from django.shortcuts import render
from django.http import HttpResponse

def index(request):
    return HttpResponse("Hello, at polls index")

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest1.serializers import UserSerializer, GroupSerializer
from rest1.models import Data
from rest1.serializers import DataSerializer

class DataViewSet(viewsets.ModelViewSet):
    queryset = Data.objects.all()
    serializer_class = DataSerializer
    print(queryset)


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