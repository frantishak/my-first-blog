from django.db import models

# Create your models here.
from django.utils import timezone


class Comment(models.Model):
    text = models.TextField()
    date_created = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User', on_delete=models.SET_NULL, null=True)

    def __repr__(self):
        return 'Comment(id={}, author={}, text={})'.format(self.id, self.author, self.text)

    def __str__(self):
        return  self.text


