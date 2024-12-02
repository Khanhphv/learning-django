import logging


class JWTAuthenticationMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and setup
        self.logger = logging.getLogger(__name__)


    def __call__(self, request):
        # Code executed for each request before the view is called
        self.logger.info(f"Incoming Request: {request.method} {request.path}")
        
        response = self.get_response(request)

        # Code executed for each response after the view is called
        self.logger.info(f"Response Status: {response.status_code} for {request.method} {request.path}")
        
        return response