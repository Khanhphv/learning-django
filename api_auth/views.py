import logging
import traceback
from os import name
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework.parsers import JSONParser
from api_auth.serializers import UserSerializer
from djangoProject.error import AppError, ErrorEnum
from djangoProject.paging import paginate_results
from .models import User
from rest_framework import status
from google.oauth2 import id_token
from rest_framework_simplejwt.tokens import RefreshToken
from google.auth.transport import requests
import os

# @csrf_exempt
# @api_view(['POST'])
def login(request):
    data = JSONParser().parse(request)
    email = data.get('email')
    password = data.get('password')
    provider = data.get('provider')
    if email and password:
        querySet = User.objects.filter(email=email, password=password).first()
    elif provider:
        token = data.get('token')
        if provider == 'google':
            CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
            print(CLIENT_ID)
            try:
                id_info = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
                
                if id_info['aud'] != CLIENT_ID:
                    return AppError(ErrorEnum.UNAUTHORIZED).to_response()
                email = id_info['email']
                querySet = User.objects.get_or_create(email=email)[0]
                querySet.provider = provider
                querySet.save()
                
            except Exception as e:
                logging.error(traceback.format_exc())
                return AppError(ErrorEnum.UNAUTHORIZED).to_response()
       
            
    if querySet is None:
        return AppError(ErrorEnum.UNAUTHORIZED).to_response()

    refresh = RefreshToken.for_user(querySet)
    return JsonResponse(
        {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        },
        status=status.HTTP_200_OK,
    )


def logout(request):
    pass


def refresh_token(request):
    pass


@paginate_results(page_size=5)
def user_list(request):
    querySet = User.objects.all()
    serializer = UserSerializer(querySet, many=True)
    return serializer.data



    