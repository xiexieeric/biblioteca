from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from json import loads, dumps
from django.core import serializers

def index(request):
	return HttpResponse('Welcome to the index page for the experience API v1')