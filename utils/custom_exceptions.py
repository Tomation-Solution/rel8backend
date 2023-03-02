from rest_framework.exceptions import PermissionDenied
from rest_framework import status

class CustomError(PermissionDenied):
    'this helps me throw custom Errors Anytime AnyDay ;)'

    
    def __init__(self, message, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = {
            'message':message,
            "status_code":status_code
        }
        self.status_code =status_code
        

    
class PaymentError(PermissionDenied):
    'this made for only interswitch payment gateway'


    def __init__(self,error_ob:dict, status_code=status.HTTP_400_BAD_REQUEST):
        self.detail = error_ob
        self.status_code =status_code
