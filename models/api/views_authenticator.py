from api.views import serialize, generate_response
from api.models import Authenticator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from random import randint

def authenticator(request):
	if request.method == 'GET':
		return __handle_authenticator_get(request)
	return generate_response()
	

def __handle_authenticator_get(request):
	try:
		user_id = request.GET['user_id']
		authenticator = __get_random_authenticator(user_id)
		authenticator.save()
		return generate_response("authenticator generated", True, obj = authenticator)
	except Exception as e:
		return generate_response(str(e), False)


def __get_random_authenticator(user_id):
	pk = randint(1, 10000000)
	while Authenticator.objects.filter(authenticator = pk).exists():
		pk = randint(1, 10000000)
	return Authenticator(authenticator = pk, user_id = user_id)

