from os import name
from django.http import JsonResponse, HttpResponse
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
    email = data["email"]
    password = data.get('password')
    name = data.get('name')
    provider = data['provider']
    if email and password:
        querySet = User.objects.filter(email=email, password=password).first()
    elif provider:
        token = data.get('id_token')
        if provider == 'google':
            CLIENT_ID = os.getenv('GOOGLE_CLIENT_ID')
            idinfo = id_token.verify_oauth2_token(token, requests.Request(), CLIENT_ID)
            if idinfo['aud'] != CLIENT_ID:
                return AppError(ErrorEnum.NOT_FOUND).to_response()
        querySet = User.objects.get_or_create(email=email)[0]
            
    if querySet is None:
        return AppError(ErrorEnum.NOT_FOUND).to_response()

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



    