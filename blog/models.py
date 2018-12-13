from django.db import models
from django.utils import timezone


class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.PROTECT)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class RestorePasswordToken(models.Model):
    token = models.CharField(max_length=32)
    expier_date = models.DateTimeField()
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)

    @property
    def is_expired(self):
        return self.expier_date > timezone.now()


