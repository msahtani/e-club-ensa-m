from django.http import HttpRequest
from django.db.models import Model

def fields(T: Model):
    return [field.name for field in T._meta.get_fields()]

def ajax(request: HttpRequest) -> bool:
    return request.META.get('HTTP_X_REQUESTED_WITH') == 'XMLHttpRequest'