from rest_framework.exceptions import APIException
from django.utils.encoding import force_str
from rest_framework import status

class CustomValidationError(APIException):
    status_code = status.HTTP_200_OK
    default_detail = 'An internal error occurred.'

    def __init__(self, detail, status_code):
        if status_code is not None:self.status_code = status_code
        if detail is not None:
            self.detail = {force_str(detail)}
        else: self.detail = {'detail': force_str(self.default_detail)}
