from django.db import models
from django.db import models
from pygments.lexers import get_all_lexers
from pygments.styles import get_all_styles
import uuid

class Data(models.Model):
    content = models.CharField(max_length=128)
    def __str__(self):
        return self.content

LEXERS = [item for item in get_all_lexers() if item[1]]
LANGUAGE_CHOICES = sorted([(item[1][0], item[0]) for item in LEXERS])
STYLE_CHOICES = sorted((item, item) for item in get_all_styles())


class Snippet(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    title = models.CharField(max_length=100, blank=True, default='')
    code = models.TextField()
    linenos = models.BooleanField(default=False)
    language = models.CharField(choices=LANGUAGE_CHOICES, default='python', max_length=100)
    style = models.CharField(choices=STYLE_CHOICES, default='friendly', max_length=100)
    id = models.CharField(max_length=64,primary_key=True)
    owner = models.ForeignKey('auth.User', related_name='snippets', on_delete=models.CASCADE,default='')
    highlighted = models.TextField(default='')
    class Meta:
        ordering = ('created',)
    def save(self,*args,**kwargs):
        if not self.id:
            self.id = uuid.uuid1().hex
        super(Snippet,self).save(*args,**kwargs)
