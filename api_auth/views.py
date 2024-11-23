from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api_auth.serializers import UserSerializer
from .models import User
from rest_framework import status

from rest_framework_simplejwt.tokens import RefreshToken

@csrf_exempt
def login(request):
    data = JSONParser().parse(request)
    email = data['email']
    password = data['password']
    print(email, password)
    querySet = User.objects.filter(email=email, password=password).first()
    serializer = UserSerializer(querySet)
    
    if querySet is None: 
        return JsonResponse({
            'data': 'notFound'
        }, status=status.HTTP_400_BAD_REQUEST)  
        
    refresh = RefreshToken.for_user(querySet)
    return JsonResponse({
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }, status=status.HTTP_200_OK)

def logout(request):
    pass


def refresh_token(request):
    pass
