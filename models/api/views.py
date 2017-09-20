from django.shortcuts import render
from django.http import HttpResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

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
