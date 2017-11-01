from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt
from datetime import datetime
from kafka import KafkaProducer

import json
from django.core import serializers
from kafka import KafkaProducer

import urllib.request as requests
import urllib.parse as parse

__MODELS_URL = 'http://models-api:8000/api/v1/'
__BOOK = 'book/'
__AUTHOR = 'author/'
__REVIEW = 'review/'
__LISTING = 'listing/'
__USER = 'user/'
__AUTHENTICATOR = 'authenticator/'

def index(request):
	return HttpResponse('Welcome to the index page for the experience API v1')


@csrf_exempt
def home(request):
	if request.method == 'GET':
		result = {
			'top_books': __get_sorted_book_results('rating', 10),
			'recent_books': __get_sorted_book_results('year_published', 10),
			'recent_listings': __get_sorted_listing_results('post_date', 10)
		}
		return __generate_response('home page data', True, result)
	else:
		return __generate_response('only GET accepted', False)


@csrf_exempt
def get_top_books(request, count):
	"""
	count - int representing number of top results to return. If greater than the size of the db, returns db.
	"""
	if request.method == 'GET':
		try:
			result = __get_sorted_book_results('rating', count)
			return __generate_response(count, True, result)

		except Exception as e:	
			return __generate_response(str(e), False)
			
	else:
		return __generate_response('only GET accepted', False)


@csrf_exempt
def get_recent_books(request, count):
	"""
	count - int representing number of results to return. If greater than the size of the db, returns db.
	"""
	if request.method == 'GET':
		try:
			result = __get_sorted_book_results('year_published', count)
			return __generate_response(count, True, result)

		except Exception as e:	
			return __generate_response(str(e), False)

	else:
		return __generate_response('only GET accepted', False)

@csrf_exempt
def get_recent_listings(request, count):
	"""
	count - int representing number of results to return. If greater than the size of the db, returns db.
	"""
	if request.method == 'GET':
		try:
			result = __get_sorted_listing_results('post_date', count)
			return __generate_response(count, True, result)

		except Exception as e:	
			return __generate_response(str(e), False)

	else:
		return __generate_response('only GET accepted', False)


def __get_sorted_book_results(key, count, reverse = True):
	"""
	Utility function for sorting books by date published and by rating
	"""
	r = __make_request(__MODELS_URL + __BOOK + 'all')
	get_result = r['result']
	sorted_result = []
	for book in get_result:
		# record the fields plus object's pk
		data = book['fields']
		data['pk'] = book['pk']
		sort_index = data[key]
		sorted_result.append((float(sort_index), data))
	sorted_result = sorted(sorted_result, key = lambda x: x[0], reverse = reverse)
	sorted_result = sorted_result[0:int(count)]
	return [data for (published, data) in sorted_result]

def __get_sorted_listing_results(key, count, reverse = True):
	"""
	Utility function for sorting books by date published and by rating
	"""
	r = __make_request(__MODELS_URL + __LISTING + 'all')
	get_result = r['result']
	sorted_result = []
	for listing in get_result:
		# record the fields plus object's pk
		data = listing['fields']
		data['pk'] = listing['pk']
		sort_index = data[key]
		sorted_result.append((sort_index, data))
	sorted_result = sorted_result[0:int(count)]
	return [data for (published, data) in sorted_result]


#Extend your experience services to have a "create account", "logout", "login" and "create new listing" service.

@csrf_exempt
def create_account(request):
	if request.method == 'POST':
		r = __make_request(
			__MODELS_URL + __USER + 'create', 
			data = request.POST, 
			method = 'POST'
		)
		return JsonResponse(r)
	else:
		return __generate_response('only POST accepted', False)


@csrf_exempt
def user_login(request):
	"""
	Logs a user in. Must not be able to log in a user if the user is already logged in AKA if authenticator for user already exists.
	Requires a user_id and plaintext password.
	"""
	if request.method == 'POST':
		# get user id from login
		auth_response = __make_request(
			__MODELS_URL + __USER + 'authenticate', 
			data = request.POST, 
			method = 'POST'
		)
		if auth_response['success']:
			token_response = __make_request(
					__MODELS_URL + __AUTHENTICATOR + 'create',
					data = {
						'user_id': auth_response['result']['pk']
					},
					method = 'POST'
				)
			token_response['msg'] = 'user authenticated successfully, returning authenticator token'
			return JsonResponse(token_response)

		else:
			return __generate_response('user_login - not able to authenticate', False)
	else:
		return __generate_response('user_login - only POST accepted', False)


@csrf_exempt
def user_logout(request):
	"""
	Requires posting the authenticator token so that the authenticator can be deleted.
	"""
	if request.method == 'POST':
		try:
			r = __make_request(__MODELS_URL + __AUTHENTICATOR + 'delete/' + request.POST['authenticator'])
			if r['success']:
				return __generate_response('user logged out successfully', True)
			else:
				return __generate_response('invalid token', False)
		except Exception as e:
			return __generate_response(str(e), False)

	else:
		return __generate_response('only POST accepted', False)


@csrf_exempt
def create_new_listing(request):
	"""
	expects params for creating the new listing as well as the auth token 'authenticator'
	authenticates using the authenticator first
	"""
	if request.method == 'POST':
		if request.POST['authenticator'] == 'all':
			return __generate_response('invalid authenticator token', False)
		auth_response = __make_request(
				__MODELS_URL + __AUTHENTICATOR + request.POST['authenticator']
			)
		if auth_response['success']:
			r =  __make_request(
					__MODELS_URL + __LISTING + 'create', 
					data = request.POST, 
					method = 'POST'
				)
			if r['success']:
				producer = KafkaProducer(bootstrap_servers='kafka:9092')
				producer.send('new-listing-topic', json.dumps(r['fields']).encode('utf-8'))
			return JsonResponse(r)
		else:
			return __generate_response('invalid authenticator token', False)
	else:
		return __generate_response('only POST accepted', False)



# Default model endpoints --------------------------------------------------

@csrf_exempt
def book(request, book_id): 
	"""
	Mirror of model book endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __BOOK + book_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __BOOK + book_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __BOOK + book_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)


@csrf_exempt
def author(request, author_id): 
	"""
	Mirror of model author endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __AUTHOR + author_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __AUTHOR + author_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __AUTHOR + author_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)


@csrf_exempt
def review(request, review_id): 
	"""
	Mirror of model review endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __REVIEW + review_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __REVIEW + review_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __REVIEW + review_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)


@csrf_exempt
def listing(request, listing_id): 
	"""
	Mirror of model listing endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __LISTING + listing_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __LISTING + listing_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __LISTING + listing_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)


@csrf_exempt
def user(request, user_id): 
	"""
	Mirror of model user endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __USER + user_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __USER + user_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __USER + user_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)


@csrf_exempt
def listing(request, listing_id): 
	"""
	Mirror of model lisintg endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __LISTING + listing_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __LISTING + listing_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __LISTING + listing_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)

@csrf_exempt
def authenticator(request, auth_id): 
	"""
	Mirror of model authenticator endpoint
	"""
	if request.method == 'GET':
		if len(request.GET) > 0:
			url = __MODELS_URL + __AUTHENTICATOR + auth_id + '?' + parse.urlencode(request.GET)
		else: 
			url = __MODELS_URL + __AUTHENTICATOR + auth_id
		r = __make_request(url)
	elif request.method == 'POST':
		r = __make_request(
				__MODELS_URL + __AUTHENTICATOR + auth_id, 
				data = request.POST, 
				method = 'POST'
			)
	return JsonResponse(r)

@csrf_exempt
def login(request):
	if request.method == 'POST':
		r = __make_request(
			__MODELS_URL + __USER + 'create',
			data = request.POST,
			method = 'POST'
		)
	return JsonResponse(r)


def __make_request(url, data = None, method = 'GET'):
	""" 
	returns loaded json
	"""
	if data:
		post_encoded = parse.urlencode(data).encode('utf-8')
		req = requests.Request(
			url, 
			data = post_encoded, 
			method = method
		)
	else:
		req = requests.Request(url)
	resp_json = requests.urlopen(req).read().decode('utf-8')
	return loads(resp_json)


def __generate_response(msg, success, data = None):
	"""
	loads the json data
	"""
	res = {}
	res["success"] = success
	res["msg"] = msg
	res["result"] = data
	return JsonResponse(res)



