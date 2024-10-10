# shops/serializers.py

from rest_framework import serializers
from .models import Shop

class ShopSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shop
        fields = ['id', 'name', 'address', 'owner_name', 'phone_number', 'email', 'latitude', 'longitude']
