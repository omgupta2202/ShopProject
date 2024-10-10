# Shops/views.py
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Shop
from .forms import ShopForm
from django.http import JsonResponse
from django.db.models import F
from math import radians, sin, cos, sqrt, atan2
from django.core.exceptions import ValidationError
import math

# Custom validation for latitude and longitude
def validate_latitude(latitude):
    if latitude < -90 or latitude > 90:
        raise ValidationError("Invalid latitude. It must be between -90 and 90.")

def validate_longitude(longitude):
    if longitude < -180 or longitude > 180:
        raise ValidationError("Invalid longitude. It must be between -180 and 180.")

# Manual shop registration view
def register_shop(request):
    if request.method == 'POST':
        # Extract values from POST request
        name = request.POST.get('name')
        address = request.POST.get('address')
        owner_name = request.POST.get('owner_name')
        phone_number = request.POST.get('phone_number')
        email = request.POST.get('email')
        latitude = float(request.POST.get('latitude'))
        longitude = float(request.POST.get('longitude'))
        
        # Manual validations
        errors = []

        # Validate latitude and longitude
        try:
            validate_latitude(latitude)
        except ValidationError as e:
            errors.append(str(e))

        try:
            validate_longitude(longitude)
        except ValidationError as e:
            errors.append(str(e))

        # Validate email
        if not email or "@" not in email:
            errors.append("Invalid email format.")
        
        # Validate phone number (simple example)
        if not phone_number.isdigit() or len(phone_number) < 10:
            errors.append("Phone number must be numeric and at least 10 digits.")
        
        # If no errors, save the shop
        if not errors:
            shop = Shop(
                name=name,
                address=address,
                owner_name=owner_name,
                phone_number=phone_number,
                email=email,
                latitude=latitude,
                longitude=longitude
            )
            shop.save()
            return redirect('shop-list')  # Redirect to shop list view

        # If there are errors, render them back to the user
        return render(request, 'shops/register.html', {
            'errors': errors,
            'values': request.POST  # To refill the form with user input
        })
    
    return render(request, 'shops/register.html')

def check_shop_name(request):
    shop_name = request.GET.get('shop_name')
    if Shop.objects.filter(name=shop_name).exists():
        return HttpResponse('taken')
    return HttpResponse('available')

# View to check if latitude and longitude are valid
def check_lat_long(request):
    latitude = float(request.GET.get('latitude', 0))
    longitude = float(request.GET.get('longitude', 0))

    # Check latitude and longitude validity
    if latitude < -90 or latitude > 90:
        return HttpResponse('invalid_lat')
    if longitude < -180 or longitude > 180:
        return HttpResponse('invalid_long')
    
    return HttpResponse('valid')

# Shop list view
def shop_list(request):
    shops = Shop.objects.all()
    return render(request, 'shops/shop_list.html', {'shops': shops})

# Helper function to calculate distance between two coordinates
def haversine(lat1, lon1, lat2, lon2):
    R = 6371  # Radius of Earth in kilometers
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)
    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))
    return R * c

# Search shops by user location
def search_shops(request):
    user_lat = float(request.GET.get('latitude'))
    user_lon = float(request.GET.get('longitude'))

    shops = Shop.objects.annotate(
        distance=(
            haversine(user_lat, user_lon, F('latitude'), F('longitude'))
        )
    ).order_by('distance')

    # Prepare JSON response with shop names and distances
    shop_list = [{'shop': shop.name, 'distance': haversine(user_lat, user_lon, shop.latitude, shop.longitude)} for shop in shops]
    return JsonResponse(shop_list, safe=False)

def haversine(lat1, lon1, lat2, lon2):
    # Convert latitude and longitude from degrees to radians
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of earth in kilometers. Use 3956 for miles
    return c * r

def search_shops(request):
    if request.method == "GET":
        user_latitude = request.GET.get('latitude')
        user_longitude = request.GET.get('longitude')

        try:
            user_latitude = float(user_latitude)
            user_longitude = float(user_longitude)
        except (ValueError, TypeError):
            return render(request, 'Shops/search.html', {'errors': ['Invalid latitude or longitude']})

        # Get all shops and calculate their distance from the user's location
        shops_with_distance = []
        for shop in Shop.objects.all():
            distance = haversine(user_latitude, user_longitude, shop.latitude, shop.longitude)
            shops_with_distance.append({'shop': shop, 'distance': distance})

        # Sort shops by distance
        sorted_shops = sorted(shops_with_distance, key=lambda x: x['distance'])

        return render(request, 'Shops/search_results.html', {'shops': sorted_shops})
    
    return render(request, 'Shops/search.html')