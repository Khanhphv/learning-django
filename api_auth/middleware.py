import logging
import traceback
from google.oauth2 import id_token
from google.auth.transport import requests
from djangoProject.error import AppError, ErrorEnum
from rest_framework_simplejwt.tokens import Token
from rest_framework_simplejwt.authentication import JWTAuthentication

class LogRequestMiddleware:
    __name__ = 'app'
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and setup
        self.logger = logging.getLogger('app')


    def __call__(self, request):
        # Code executed for each request before the view is called
        self.logger.info(f"Incoming Request: {request.method} {request.path}")
        
        response = self.get_response(request)

        # Code executed for each response after the view is called
        self.logger.info(f"Response Status: {response.status_code} for {request.method} {request.path}")
        
        return response
    

class AuthenticationMiddleware(LogRequestMiddleware):

    def __init__(self, get_response):
         super().__init__(get_response)
    
    def __call__(self, request):
        print(request.path)
        protected_routes = [
            '/api/user-list',
        ]
        if(request.path in protected_routes):
            access_token = request.headers.get('Authorization')
            if not access_token:
                return AppError(ErrorEnum.UNAUTHORIZED).to_response()
            try:
                JWT_authenticator = JWTAuthentication()
                validated_token = JWT_authenticator.get_validated_token(access_token)
                user = JWT_authenticator.get_user(validated_token)
                if user is None:
                    return AppError(ErrorEnum.UNAUTHORIZED).to_response()
            except Exception as e:
                self.logger.error(traceback.format_exc())
                return AppError(ErrorEnum.UNAUTHORIZED).to_response()
        
        response = self.get_response(request)
        return response