from django.http import HttpRequest
from django.db.models import Model

def fields(T: Model, exclude=[]):
    return [
        field.name for field in T._meta.get_fields()
        if field.name not in exclude
    ]

def ajax(request: HttpRequest) -> bool:
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'


def get_full_name():
    pass