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


def generate_response(res, msg, obj=None):
	if obj is None:
		res["success"] = False
		res["msg"] = msg
	else:
		res["result"] = serialize(obj)
		res["success"] = True
		res["msg"] = msg
	return HttpResponse(dumps(res))


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
			return generate_response(res, author, "author found")
		except:
			return generate_response(res, "author not found")

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
			return generate_response(res, author, "author updated")
		except:
			return generate_response(res, "author not found")


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
			return generate_response(res, author, "author created")

		# Print the exception if we run into one.
		except Exception as e:
			return generate_response(res, e)

	# We only accept POST requests to this endpoint.
	return generate_response(res, "only POST requests are allowed")


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
			book = Book.objects.get(pk=book_id)
			return generate_response(res, book, "book found")
		except:
			return generate_response(res, "book not found")

	if request.method == 'POST':
		try:
			book = Book.objects.get(pk=book_id)
			for key in request.POST:
				value = request.POST[key]
				if key == 'title':
					book.title = value
				elif key == 'year_published':
					book.year_published = value
				elif key == 'rating':
					book.rating = value
				elif key == 'author':
					book.author = value
			book.save()
			return generate_response(res, book, "book updated")
		except:
			return generate_response(res, "book not found")


@csrf_exempt
def create_book(request):
	"""
	Handles the /book/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
	if request.method == 'POST':

		# Try to parse values and save to database
		try:
			title = request.POST['title']
			year_published = request.POST['year_published']
			rating = request.POST['rating']
			author_id = request.POST['author']
			author = Author.objects.get(pk=author_id)
			book = Book(
				title = title, 
				year_published = year_published,
				rating = rating,
				author = author,
				)
			book.save()
			return HttpResponse("Saved Book successfully.")

		# Print the exception if we run into one.
		except Exception as e:
			return HttpResponse(e)

	# We only accept POST requests to this endpoint.
	return HttpResponse("400 - Bad request, make sure to POST")


@csrf_exempt
def delete_book(request, book_id):
	try:
		book = Book.objects.get(pk=book_id)
		book.delete()
		return HttpResponse('{\"status\": \"ok, book deleted successfully\"}')
	except:
		return HttpResponse('{\"status\": \"error, book does not exist\"}')


@csrf_exempt
def review(request, review_id):
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
			review = Review.objects.get(pk=review_id)
			return generate_response(res, review, "review found")
		except:
			return generate_response(res, "review not found")

	if request.method == 'POST':
		try:
			review = Review.objects.get(pk=review_id)
			for key in request.POST:
				value = request.POST[key]
				if key == 'reviewer':
					review.reviewer = value
				elif key == 'pub_date':
					review.pub_date = value
				elif key == 'book':
					review.book = value
				elif key == 'rating':
					review.rating = value
				elif key == 'content':
					review.content = value
			review.save()
			return generate_response(res, review, "review updated")
		except:
			return generate_response(res, "review not found")


@csrf_exempt
def create_review(request):
	"""
	Handles the /review/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
	if request.method == 'POST':

		# Try to parse values and save to database
		try:
			reviewer = request.POST['reviewer']
			book_id = request.POST['book']
			book = Book.objects.get(pk=book_id)			
			rating = request.POST['rating']
			content = request.POST['content']
			review = Review(
				reviewer = reviewer, 
				book = book,
				rating = rating,
				content = content,
				)
			review.save()
			return HttpResponse("Saved Review successfully.")

		# Print the exception if we run into one.
		except Exception as e:
			return HttpResponse(e)

	# We only accept POST requests to this endpoint.
	return HttpResponse("400 - Bad request, make sure to POST")


@csrf_exempt
def delete_review(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
		review.delete()
		return HttpResponse('{\"status\": \"ok, review deleted successfully\"}')
	except:
		return HttpResponse('{\"status\": \"error, review does not exist\"}')













