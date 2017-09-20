from django.shortcuts import render
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from api.models import Author, Book, Review

# Create your views here.

def index(request):
	return HttpResponse('Welcome to the index page for API v1')


@csrf_exempt
def author(request, author_id):
	if request.method == 'GET':
		# Need to get the csrf token and add as a header in postman POST request
		# for key X-CSRFToken for post requests to work
		#return HttpResponse(get_token(request))
		return HttpResponse('GET ' + author_id)
	if request.method == 'POST':
		return HttpResponse('POST ' +  author_id)

@csrf_exempt
def create_author(request):
	"""
	Handles the /author/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
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
			return HttpResponse("Saved successfully.")

		# Print the exception if we run into one.
		except Exception as e:
			return HttpResponse(e)

	# We only accept POST requests to this endpoint.
	return HttpResponse("400 - Bad request, make sure to POST")


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