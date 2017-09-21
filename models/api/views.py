from django.shortcuts import render
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt


from api.models import Author, Book, Review

from json import loads, dumps
from django.core import serializers



# Create your views here.

def index(request):
	return HttpResponse('Welcome to the index page for API v1')


def serialize(obj):
	"""
	Easy json serialization for a single object.
	"""
	serialized = serializers.serialize('json', [obj])
	data = loads(serialized)
	return data[0] # Cuts off the first and last char '[' and ']' to match assignment format.


@csrf_exempt
def author(request, author_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	res = {}
	if request.method == 'GET':
		# Need to GET the csrf token and add as a header in postman POST request
		# for key X-CSRFToken for post requests to work
		#return HttpResponse(get_token(request))
		try:
			author = Author.objects.get(pk=author_id)
			res["success"] = True
			res["msg"] = "Author found"
			res["result"] = serialize(author)
			return HttpResponse(dumps(res))
		except:
			res["success"] = False
			res["msg"] = "Author does not exist"
			return HttpResponse(dumps(res))

	if request.method == 'POST':
		try:
			author = Author.objects.get(pk=author_id)
			for key in request.POST:
				value = request.POST[key]
				if key == 'first_name':
					author.first_name = value
				elif key == 'last_name':
					author.last_name = value
				elif key == 'age':
					author.age = value
			author.save()
			res["success"] = True
			res["msg"] = "Author updated"
			res["result"] = serialize(author)
			return HttpResponse(dumps(res))
		except:
			res["success"] = False
			res["msg"] = "Author does not exist"
			return HttpResponse(dumps(res))

@csrf_exempt
def create_author(request):
	"""
	Handles the /author/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
	res = {}
	if request.method == 'POST':

		# Try to parse values and save to database
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
			res["success"] = True
			res["msg"] = "Author created"
			res["result"] = serialize(author)
			return HttpResponse(dumps(res))

		# Print the exception if we run into one.
		except Exception as e:
			res["success"] = False
			res["msg"] = e
			return HttpResponse(dumps(res))

	# We only accept POST requests to this endpoint.
	return HttpResponse('{\"status\": \"error, only POST is allowed\"}')


@csrf_exempt
def delete_author(request, author_id):
	try:
		author = Author.objects.get(pk=author_id)
		author.delete()
		return HttpResponse('{\"status\": \"ok, author deleted successfully\"}')
	except:
		return HttpResponse('{\"status\": \"error, author does not exist\"}')


@csrf_exempt
def book(request, book_id):
	if request.method == 'GET':
		return HttpResponse('GET ' + book_id)
	if request.method == 'POST':
		return HttpResponse('POST ' +  book_id)


@csrf_exempt
def review(request, review_id):
	if request.method == 'GET':
		return HttpResponse('GET ' + review_id)
	if request.method == 'POST':
		return HttpResponse('POST ' +  review_id)