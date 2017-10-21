from api.views import serialize, generate_response
from api.models import User, Authenticator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import make_password, check_password

from random import randint


@csrf_exempt
def create_user(request):
	"""
	Handles the /user/create endpoint for creating an user and adding it to the database.
	"""
	if request.method == 'POST': 
		return __handle_create_user_post(request)
	return generate_response("only POST requests are allowed", False)


def __handle_create_user_post(request):
	try:
		username = request.POST['username']
		matching_usernames = User.objects.get(username = username)
		if matching_usernames:
			return generate_response("username already exists", False)

		password = make_password(request.POST['password'])
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		user = User(
			username = username,
			password = password,
			first_name = first_name, 
			last_name = last_name
		)
		user.save()
		return generate_response("user created", True, user)
	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def authenticate_user(request):
	"""
	Authenticates a user using their password and returns success if authenticated
	"""
	if request.method == 'POST': 
		return __handle_authenticate_user_post(request)
	return generate_response("only POST requests are allowed", False)


def __handle_authenticate_user_post(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		result = User.objects.get(username = username, password = password)
		return generate_response("user authenticated", True)
	except Exception as e:
		return generate_response(str(e), False)




