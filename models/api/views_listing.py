from api.views import serialize, generate_response

from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q

from api.models import User, Listing, Book

@csrf_exempt
def listing(request, listing_id):
	"""
	GET - return the row in the corresponding database table in JSON.
	POST - be able to update a row in the table given a set of key-value form encoded pairs (PREFERRED, NOT JSON)
	"""
	if request.method == 'GET':
		return __handle_listing_get(request, listing_id)
	if request.method == 'POST':
		return __handle_listing_post(request, listing_id)


def __handle_listing_get(request, listing_id):
	if listing_id == 'all':
		result = __filter(Listing.objects.all(), request.GET)
		if len(result) == 0: 
			return generate_response("no queries matched filters", True, payload = {"result": []})
		else: 
			return generate_response("found results", True, obj_list = list(result))
	else:
		try:
			listing = Listing.objects.get(pk=listing_id)
			return generate_response("listing found", True, listing)
		except:
			return generate_response("listing not found", False)


def __filter(query_set, filters):
	for key in filters:
		value = filters[key]
		if key == 'id': query_set = query_set.filter(id = value)
		elif key == 'lister': query_set = query_set.filter(lister__exact = value)
		elif key == 'post_date': query_set = query_set.filter(post_date__exact = value)
		elif key == 'price': query_set = query_set.filter(price__gte = value)
		elif key == 'book': 
			if value.isdigit():
				query_set = query_set.filter(book__id = int(value))
			else:
				query_set = query_set.filter(book__title__icontains = value)
	return query_set


def __handle_listing_post(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
		for key in request.POST:
			value = request.POST[key]
			if key == 'lister':
				user = User.objects.get(pk=value)
				listing.lister = user
			elif key == 'post_date':
				listing.post_date = value
			elif key == 'book':
				book = Book.objects.get(pk=value)	
				listing.book = book
				listing.book_title = book.title
			elif key == 'price':
				listing.price = value
		listing.save()
		return generate_response("listing updated", True, listing)
	except:
		return generate_response("listing not found", False)


@csrf_exempt
def create_listing(request):
	"""
	Handles the /listing/create endpoint for creating a listing and adding it to the database.
	"""
	if request.method == 'POST':
		return __handle_create_listing_post(request)
	return generate_response("Only POST requests allowed", False)


def __handle_create_listing_post(request):
	try:
		user_id = request.POST['lister']
		lister = User.objects.get(pk=user_id)
		book_id = request.POST['book']
		book = Book.objects.get(pk=book_id)
		price = request.POST['price']
		listing = Listing(
			lister = lister, 
			book = book,
			price = price,
			book_title = book.title,
		)
		listing.save()
		return generate_response("listing saved", True, listing)
	except KeyError as e:
		return generate_response("missing %s" % e.args[0].strip("'"), False)
	except Exception as e:
		return generate_response(str(e), False)


@csrf_exempt
def delete_listing(request, listing_id):
	try:
		listing = Listing.objects.get(pk=listing_id)
		listing.delete()
		return generate_response("listing deleted", True, listing)
	except:
		return generate_response("listing does not exist", False)


