from django.db import models
from django.db import models


class Data(models.Model):
    content = models.CharField(max_length=128)
