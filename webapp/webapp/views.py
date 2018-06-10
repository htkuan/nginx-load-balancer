import os
from django.http import HttpResponse


def index(request):
    return HttpResponse(os.environ.get('APP'))
