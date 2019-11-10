from django.db import models


class Datapoint(models.Model):
    locLat = models.CharField(max_length=200)
    locLong = models.CharField(max_length=200)
