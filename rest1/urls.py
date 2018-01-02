#!/usr/bin/env python
#coding:utf-8
from django.urls import path,include
from rest_framework.routers import DefaultRouter
from .views import DataViewSet
router = DefaultRouter()
router.register(prefix='data',viewset=DataViewSet)

urlpatterns = [
    path('', include(router.urls))
]