from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from api.models import Author, Book, Review

from json import loads, dumps
from django.core import serializers


def index(request):
	return HttpResponse('Welcome to the index page for API v1')


def serialize(obj):
	"""
	Easy json serialization for a single object.
	"""
	serialized = serializers.serialize('json', [obj])
	data = loads(serialized)
	return data[0] # Cuts off the first and last char '[' and ']' to match assignment format.


def generate_response(msg, success, obj=None, li=None):
	res = {}
	res["success"] = success
	res["msg"] = msg
	if obj: res["result"] = serialize(obj)
	elif li:
		json_list = []
		for entry in li:
			json_list.append(serialize(entry))
		res["result"] = json_list
	return JsonResponse(res)


@csrf_exempt
def author(request, author_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		if author_id == 'all':
			all_authors = list(Author.objects.all())
			return generate_response("all authors", True, li=all_authors)
		try:
			author = Author.objects.get(pk=author_id)
			return generate_response("author found", True, author)
		except:
			return generate_response("author not found", False)

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
			return generate_response("author created", True, author)

		# Print the exception if we run into one.
		except Exception as e:
			return generate_response(str(e), False)

	# We only accept POST requests to this endpoint.
	return generate_response("only POST requests are allowed", False)


@csrf_exempt
def delete_author(request, author_id):
	try:
		author = Author.objects.get(pk=author_id)
		author.delete()
		return generate_response("author deleted", True, author)
	except:
		return generate_response("author not found", False)


@csrf_exempt
def book(request, book_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		if book_id == 'all':
			all_books = list(Book.objects.all())
			return generate_response("all book", True, li=all_books)
		try:
			book = Book.objects.get(pk=book_id)
			return generate_response("book found", True, book)
		except:
			return generate_response("book not found", False)

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
					author = Author.objects.get(pk=value)	
					book.author = author
			book.save()
			return generate_response("book updated", True, book)
		except:
			return generate_response("book not found", False)


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
			return generate_response("book saved", True, book)

		# Print the exception if we run into one.
		except Exception as e:
			return generate_response(str(e), False)

	# We only accept POST requests to this endpoint.
	return generate_response("Only POST requests allowed", False)


@csrf_exempt
def delete_book(request, book_id):
	try:
		book = Book.objects.get(pk=book_id)
		book.delete()
		return generate_response("book deleted", True, book)
	except:
		return generate_response("book does not exist", False)


@csrf_exempt
def review(request, review_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		if review_id == 'all':
			all_reviews = list(Review.objects.all())
			return generate_response("all reviews", True, li=all_reviews)
		try:
			review = Review.objects.get(pk=review_id)
			return generate_response("review found", True, review)
		except:
			return generate_response("review not found", False)

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
					book = Book.objects.get(pk=value)	
					review.book = book
				elif key == 'rating':
					review.rating = value
				elif key == 'content':
					review.content = value
			review.save()
			return generate_response("review updated", True, review)
		except:
			return generate_response("review not found", False)


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
			return generate_response("review saved", True, review)

		# Print the exception if we run into one.
		except Exception as e:
			return generate_response(str(e), False)

	# We only accept POST requests to this endpoint.
	return generate_response("Only POST requests allowed", False)


@csrf_exempt
def delete_review(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
		review.delete()
		return generate_response("review deleted", True, review)
	except:
		return generate_response("review does not exist", False)













