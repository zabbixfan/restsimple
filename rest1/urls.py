#!/usr/bin/env python
#coding:utf-8
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DataViewSet
# from .views import ListUsers
from .views import SnippetList,SnippetDetail
from .views import *
# router = DefaultRouter()
# router.register(prefix='data',viewset=DataViewSet)

urlpatterns = [
    # path('', include(router.urls)),
    path('users/',UserList.as_view()),
    path('users/<int:pk>/',UserDetail.as_view()),
    # path('data1',ListUsers.as_view()),
    path('snippets',SnippetList.as_view()),
    path('snippets/<int:pk>/',SnippetDetail.as_view()),
    path('simple/',SimpleView.as_view())
]