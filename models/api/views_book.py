from api.views import serialize, generate_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from api.models import Book, Author

@csrf_exempt
def book(request, book_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		return __handle_book_get(request, book_id)
	if request.method == 'POST':
		return __handle_book_post(request, book_id)


def __handle_book_get(request, book_id):
	if book_id == 'all':
		result = __filter(Book.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))
	else:
		try:
			book = Book.objects.get(pk=book_id)
			return generate_response("book found", True, book)
		except:
			return generate_response("book not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
		elif key == 'title': query_set = query_set.filter(title__icontains = value)
		elif key == 'rating': query_set = query_set.filter(rating__gte = value)
		elif key == 'year_published': query_set = query_set.filter(year_published__exact = value)
		elif key == 'author': 
			if value.isdigit():
				query_set = query_set.filter(author__id = int(value))
			else:
				query_set = query_set.filter(Q(author__last_name__icontains = value) | Q(author__first_name__icontains = value))
	return query_set


def __handle_book_post(request, book_id):
	try:
		book = Book.objects.get(pk = book_id)
		for key in request.POST:
			value = request.POST[key]
			if key == 'title':
				book.title = value
			elif key == 'year_published':
				book.year_published = value
			elif key == 'rating':
				book.rating = value
			elif key == 'author':
				author = Author.objects.get(pk = value)	
				book.author = author
		book.save()
		return generate_response("book updated", True, book)
	except:
		return generate_response("error while updating book", False)


@csrf_exempt
def create_book(request):
	"""
	Handles the /book/create endpoint for creating an author and adding it to the database.
	This currently accepts the preferred method of key-value form data as stated in the 
	Project 2 description.
	"""
	if request.method == 'POST':
		return __handle_create_book_post(request)
	return generate_response("Only POST requests allowed", False)


def __handle_create_book_post(request):
	try:
		title = request.POST['title']
		year_published = request.POST['year_published']
		rating = request.POST['rating']
		author_id = request.POST['author']
		author = Author.objects.get(pk = author_id)
		book = Book(
			title = title, 
			year_published = year_published,
			rating = rating,
			author = author,
		)
		book.save()
		return generate_response("book saved", True, book)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_book(request, book_id):
	try:
		book = Book.objects.get(pk=book_id)
		book.delete()
		return generate_response("book deleted", True, book)
	except:
		return generate_response("book does not exist", False)
