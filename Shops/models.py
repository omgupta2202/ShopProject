# Shops/models.py

from django.db import models

class Shop(models.Model):
    name = models.CharField(max_length=100)
    address = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.name
