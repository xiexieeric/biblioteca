from api.views import serialize, generate_response
from api.models import Authenticator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

import hmac, os

from models import settings

@csrf_exempt
def authenticator(request, authenticator_id):
	"""
	Lookup an authenticator with its pk.
	return success True if found, else False
	"""
	if request.method == 'GET':
		return __handle_authenticator_get(request, authenticator_id)
	return generate_response("only GET requests are allowed", False)
	

def __handle_authenticator_get(request, authenticator_id):
	if authenticator_id == 'all':
		result = Authenticator.objects.all()
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))

	else:
		try:
			authenticator = Authenticator.objects.get(pk=authenticator_id)
			return generate_response("authenticator found", True, authenticator)
		except:
			return generate_response("authenticator not found", False)


@csrf_exempt
def create_authenticator(request):
	"""
	Handles the /authenticator/create endpoint for creating an authenticator and adding it to the database.
	Must POST the user_id to associate with the authenticator
	"""
	if request.method == 'POST': 
		return __handle_create_authenticator_post(request)
	return generate_response("only POST requests are allowed", False)


def __handle_create_authenticator_post(request):
	try:
		user_id = request.POST['user_id']
		authenticator = __get_random_authenticator(user_id)
		authenticator.save()
		return generate_response("authenticator generated", True, obj = authenticator)
	except Exception as e:
		return generate_response(str(e), False)


def __get_random_authenticator(user_id):
	pk = __generate_random_string()
	while Authenticator.objects.filter(authenticator = pk).exists():
		pk = __generate_random_string()
	return Authenticator(authenticator = pk, user_id = user_id)

def __generate_random_string():
	return hmac.new(
			key = settings.SECRET_KEY.encode('utf-8'),
			msg = os.urandom(32),
			digestmod = 'sha256'
		).hexdigest()

@csrf_exempt
def delete_authenticator(request, authenticator_id):
	"""
	Delete authenticator with the specified primary key
	"""
	try:
		authenticator = Authenticator.objects.get(pk=authenticator_id)
		authenticator.delete()
		return generate_response("authenticator deleted", True, authenticator)
	except:
		return generate_response("authenticator not found", False)



