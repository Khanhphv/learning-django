from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework import status
from rest_framework.parsers import JSONParser

from api.models import User
from api.serializers.UserSerializer import UserSerializer


@csrf_exempt
def user_list(request):
    if request.method == 'GET':
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        return JsonResponse(serializer.data, safe=False)
    elif request.method == 'POST':
        data = JSONParser().parse(request)
        serializer = UserSerializer(data=data)
        if serializer.is_valid():
            serializer.create(data)
            return JsonResponse(serializer.data, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@csrf_exempt
def login(request):
    data = JSONParser().parse(request)
    email = data.get('email')
    password = data.get('password')
    user = User.objects.filter(email=email, password=password).first()
    serializer = UserSerializer(user)
    if user is not None:
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    return JsonResponse({'error': 'Email or password incorrect'}, status=status.HTTP_400_BAD_REQUEST)
