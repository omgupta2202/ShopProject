from django.http import JsonResponse, HttpResponse
from django.shortcuts import redirect
from .models import Shop
from django.core.exceptions import ValidationError
from rest_framework.decorators import api_view
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
import math

def validate_latitude(latitude):
    if latitude < -90 or latitude > 90:
        raise ValidationError("Invalid latitude. It must be between -90 and 90.")

def validate_longitude(longitude):
    if longitude < -180 or longitude > 180:
        raise ValidationError("Invalid longitude. It must be between -180 and 180.")

@swagger_auto_schema(
    method='post',
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            'name': openapi.Schema(type=openapi.TYPE_STRING),
            'address': openapi.Schema(type=openapi.TYPE_STRING),
            'owner_name': openapi.Schema(type=openapi.TYPE_STRING),
            'phone_number': openapi.Schema(type=openapi.TYPE_STRING),
            'email': openapi.Schema(type=openapi.TYPE_STRING),
            'latitude': openapi.Schema(type=openapi.TYPE_NUMBER),
            'longitude': openapi.Schema(type=openapi.TYPE_NUMBER),
        },
        required=['name', 'address', 'owner_name', 'phone_number', 'email', 'latitude', 'longitude']
    )
)
@api_view(['POST'])
def register_shop(request):
    if request.method == 'POST':
        name = request.data.get('name')
        address = request.data.get('address')
        owner_name = request.data.get('owner_name')
        phone_number = request.data.get('phone_number')
        email = request.data.get('email')
        latitude = float(request.data.get('latitude'))
        longitude = float(request.data.get('longitude'))

        errors = []

        try:
            validate_latitude(latitude)
        except ValidationError as e:
            errors.append(str(e))

        try:
            validate_longitude(longitude)
        except ValidationError as e:
            errors.append(str(e))

        if not email or "@" not in email:
            errors.append("Invalid email format.")

        if not phone_number.isdigit() or len(phone_number) < 10:
            errors.append("Phone number must be numeric and at least 10 digits.")

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
            return JsonResponse({'message': 'Shop registered successfully.'}, status=201)  

        return JsonResponse({'errors': errors}, status=400)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('shop_name', openapi.IN_QUERY, description="Name of the shop to check", type=openapi.TYPE_STRING)
    ]
)
@api_view(['GET'])
def check_shop_name(request):
    shop_name = request.GET.get('shop_name')
    if Shop.objects.filter(name=shop_name).exists():
        return JsonResponse({'status': 'taken'})
    return JsonResponse({'status': 'available'})

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('latitude', openapi.IN_QUERY, description="Latitude to check", type=openapi.TYPE_NUMBER),
        openapi.Parameter('longitude', openapi.IN_QUERY, description="Longitude to check", type=openapi.TYPE_NUMBER)
    ]
)
@api_view(['GET'])
def check_lat_long(request):
    latitude = float(request.GET.get('latitude', 0))
    longitude = float(request.GET.get('longitude', 0))

    if latitude < -90 or latitude > 90:
        return JsonResponse({'status': 'invalid_lat'}, status=400)
    if longitude < -180 or longitude > 180:
        return JsonResponse({'status': 'invalid_long'}, status=400)
    
    return JsonResponse({'status': 'valid'})

@swagger_auto_schema(method='get')
@api_view(['GET'])
def shop_list(request):
    shops = Shop.objects.all().values('name', 'owner_name', 'phone_number', 'email', 'address', 'latitude', 'longitude')
    return JsonResponse(list(shops), safe=False)

def haversine(lat1, lon1, lat2, lon2):
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1 
    dlat = lat2 - lat1 
    a = math.sin(dlat / 2)**2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2)**2
    c = 2 * math.asin(math.sqrt(a)) 
    r = 6371  # Radius of Earth in kilometers
    return round(c * r, 2)

@swagger_auto_schema(
    method='get',
    manual_parameters=[
        openapi.Parameter('latitude', openapi.IN_QUERY, description="User's latitude", type=openapi.TYPE_NUMBER),
        openapi.Parameter('longitude', openapi.IN_QUERY, description="User's longitude", type=openapi.TYPE_NUMBER)
    ]
)
@api_view(['GET'])
def search_shops(request):
    user_latitude = request.GET.get('latitude')
    user_longitude = request.GET.get('longitude')

    try:
        user_latitude = float(user_latitude)
        user_longitude = float(user_longitude)
    except (ValueError, TypeError):
        return JsonResponse({'error': 'Invalid latitude or longitude'}, status=400)

    shops_with_distance = []
    for shop in Shop.objects.all():
        distance = haversine(user_latitude, user_longitude, shop.latitude, shop.longitude)
        shops_with_distance.append({'shop': shop.name, 'distance': distance})

    sorted_shops = sorted(shops_with_distance, key=lambda x: x['distance'])

    return JsonResponse(sorted_shops, safe=False)
