from api.views import serialize, generate_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from api.models import Author

@csrf_exempt
def author(request, author_id):
	"""
	GET - return either a filtered list of authors or a single author.
		/author_id : get a single author by ID
		/all?p : filter all authors by query parameters
	POST - update a single author
		/author_id : the author to update
	"""
	if request.method == 'GET':
		return __handle_author_get(request, author_id)
	elif request.method == 'POST':
		return __handle_author_post(request, author_id)


def __handle_author_get(request, author_id):
	if author_id == 'all':
		result = __filter(Author.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))

	else:
		try:
			author = Author.objects.get(pk=author_id)
			return generate_response("author found", True, author)
		except:
			return generate_response("author not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
		elif key == 'first_name': query_set = query_set.filter(first_name__icontains = value)
		elif key == 'last_name': query_set = query_set.filter(last_name__icontains = value)
		elif key == 'age': query_set = query_set.filter(age__exact = value)
	return query_set


def __handle_author_post(request, author_id):
	"""
	For updating author
	"""
	try:
		author = Author.objects.get(pk = author_id)
		for key in request.POST:
			value = request.POST[key]
			if key == 'first_name': author.first_name = value
			elif key == 'last_name': author.last_name = value
			elif key == 'age': author.age = value
		author.save()
		return generate_response("author updated", True, author)
	except:
		return generate_response("author not found", False)


@csrf_exempt
def create_author(request):
	"""
	Handles the /author/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
	if request.method == 'POST': 
		return __handle_create_author_post(request)
	return generate_response("only POST requests are allowed", False)


def __handle_create_author_post(request):
	try:
		first_name = request.POST['first_name']
		last_name = request.POST['last_name']
		age = request.POST['age']
		author = Author(
			first_name = first_name, 
			last_name = last_name, 
			age = age
		)
		author.save()
		return generate_response("author created", True, author)
	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_author(request, author_id):
	"""
	Delete author with the specified primary key
	"""
	try:
		author = Author.objects.get(pk=author_id)
		author.delete()
		return generate_response("author deleted", True, author)
	except:
		return generate_response("author not found", False)

