from enum import Enum
from http.client import NOT_FOUND
from os import error

from django.http import JsonResponse


class ErrorEnum(Enum):
    NOT_FOUND = ("Resource not found", 404)
    UNAUTHORIZED = ("Unauthorized access", 401)
    VALIDATION_ERROR = ("Invalid input data", 422)
    BAD_REQUEST = ("Bad request", 400)
    FORBIDDEN = ("Forbidden", 403)

   
    def __init__(self, message, status_code):
        self.message = message
        self.status_code = status_code

class AppError:
    def __init__(self, error: ErrorEnum):
        self.message = error.message
        self.status_code = error.status_code

    def to_dict(self):
        """
        Convert error details to a dictionary for JSON responses.
        """
        return {"error": self.message, "status_code": self.status_code}

    def to_response(self):
        """
        Convert error details to a Django JsonResponse.
        """
        return JsonResponse(self.to_dict(), status=self.status_code)