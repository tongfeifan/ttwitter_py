from django.db import models
from django.contrib.auth.models import User


class UserProfile(User):
    nickname = models.CharField(null=True, blank=True, max_length=64)
    follows = models.ManyToManyField('self', related_name='followed_by', symmetrical=False)



class UserPost(models.Model):
    content = models.CharField(max_length=140)
    user = models.ForeignKey(UserProfile)
    creation_date = models.DateTimeField(auto_now=True, blank=True)