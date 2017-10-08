from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from json import loads, dumps
from django.core import serializers

import urllib.request as requests
import urllib.parse as parse

__MODELS_URL = 'http://models-api:8000/api/v1/'
__BOOK = 'book/'
__AUTHOR = 'author/'
__REVIEW = 'review/'

def index(request):
	return HttpResponse('Welcome to the index page for the experience API v1')


@csrf_exempt
def home(request):
	if request.method == 'GET':
		result = {
			'top_books': __get_sorted_book_results('rating', 10),
			'recent_books': __get_sorted_book_results('year_published', 10)
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


def __get_sorted_book_results(key, count, reverse = True):
	r = __make_request(__MODELS_URL + __BOOK + 'all')
	get_result = r['result']
	sorted_result = []
	for book in get_result:
		data = book['fields']
		index = data[key]
		sorted_result.append((float(index), data))
	sorted_result = sorted(sorted_result, key = lambda x: x[0], reverse = reverse)
	sorted_result = sorted_result[0:int(count)]
	return [data for (published, data) in sorted_result]


def __make_request(url, data = None, method = 'GET'):
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
	res = {}
	res["success"] = success
	res["msg"] = msg
	res["result"] = data
	return JsonResponse(res)
