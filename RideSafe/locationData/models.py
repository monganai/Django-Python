from django.db import models


class Post(models.Model):
    locLat = models.CharField(max_length=200)
    locLong = models.CharField(max_length=200)
