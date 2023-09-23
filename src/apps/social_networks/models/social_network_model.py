from django.db import models
from ...user_managment.models import Profile


class SocialNetwork(models.Model):
    social_network_link = models.CharField(max_length=50)
    user = models.ForeignKey(Profile, on_delete=models.CASCADE)
    