from api.views import serialize, generate_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from api.models import Review, Book

@csrf_exempt
def review(request, review_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		return __handle_review_get(request, review_id)
	if request.method == 'POST':
		return __handle_review_post(request, review_id)


def __handle_review_get(request, review_id):
	if review_id == 'all':
		result = __filter(Review.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))
	else:
		try:
			review = Review.objects.get(pk=review_id)
			return generate_response("review found", True, review)
		except:
			return generate_response("review not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
		elif key == 'reviewer': query_set = query_set.filter(reviewer__exact = value)
		elif key == 'pub_date': query_set = query_set.filter(pub_date__exact = value)
		elif key == 'rating': query_set = query_set.filter(rating__gte = value)
		elif key == 'content': query_set = query_set.filter(content__contains = value)
		elif key == 'book': 
			if value.isdigit():
				query_set = query_set.filter(book__id = int(value))
			else:
				query_set = query_set.filter(book__title__icontains = value)
	return query_set


def __handle_review_post(request, review_id):
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
		return __handle_create_review_post(request)
	return generate_response("Only POST requests allowed", False)


def __handle_create_review_post(request):
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
	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_review(request, review_id):
	try:
		review = Review.objects.get(pk=review_id)
		review.delete()
		return generate_response("review deleted", True, review)
	except:
		return generate_response("review does not exist", False)


