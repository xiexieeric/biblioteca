from api.views import serialize, generate_response
from api.models import User, Authenticator

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import hashers

from random import randint


@csrf_exempt
def user(request, user_id):
	"""
	GET - return either a filtered list of users or a single user.
		/user_id : get a single user by ID
		/all?p : filter all users by query parameters
	POST - update a single user
		/user_id : the user to update
	"""
	if request.method == 'GET':
		return __handle_user_get(request, user_id)
	elif request.method == 'POST':
		return __handle_user_post(request, user_id)


def __handle_user_get(request, user_id):
	if user_id == 'all':
		result = __filter(User.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))

	else:
		try:
			user = User.objects.get(pk=user_id)
			return generate_response("user found", True, user)
		except:
			return generate_response("user not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
		elif key == 'first_name': query_set = query_set.filter(first_name__icontains = value)
		elif key == 'last_name': query_set = query_set.filter(last_name__icontains = value)
		elif key == 'username': query_set = query_set.filter(username__icontains = value)
		elif key == 'password': query_set = query_set.filter(password__icontains = value)
	return query_set


def __handle_user_post(request, user_id):
	"""
	For updating a user. Users cannot change their username.
	"""
	try:
		user = User.objects.get(pk = user_id)
		for key in request.POST:
			value = request.POST[key]
			if key == 'first_name': user.first_name = value
			elif key == 'last_name': user.last_name = value
			elif key == 'password': user.password = hashers.make_password(value)
		user.save()
		return generate_response("user updated", True, user)
	except:
		return generate_response("user not found", False)



@csrf_exempt
def create_user(request):
	"""
	Handles the /user/create endpoint for creating an user and adding it to the database.
	"""
	if request.method == 'POST': 
		return __handle_create_user_post(request)
	else:
		return generate_response("only POST requests are allowed", False)


def __handle_create_user_post(request):
	"""
	Creates a new user with a hashed password. Success is false if the username already exists.
	"""
	try:
		username = request.POST['username']
		if not User.objects.filter(username = username).exists():
			password = hashers.make_password(request.POST['password'])
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
		else:
			return generate_response("username already exists", False)

	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def authenticate_user(request):
	"""
	Authenticates a user using their plaintext password and returns success: True if authenticated successfully.
	"""
	if request.method == 'POST': 
		return __handle_authenticate_user_post(request)
	return generate_response("only POST requests are allowed", False)


def __handle_authenticate_user_post(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		result = User.objects.get(username = username)
		correct_password = hashers.check_password(password, result.password)
		if correct_password:
			return generate_response("user authenticated", True)
		else:
			return generate_response("incorrect username or password", False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_user(request, user_id):
	"""
	Delete user with the specified primary key
	"""
	try:
		user = User.objects.get(pk=user_id)
		user.delete()
		return generate_response("user deleted", True, user)
	except:
		return generate_response("user not found", False)




