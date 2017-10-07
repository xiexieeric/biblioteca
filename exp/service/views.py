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
def get_top_books(request, top):
	"""
	top - int representing number of top results to return. If greater than the size of the db, returns db.
	"""
	if request.method == 'GET':
		try:
			r = __make_request(__MODELS_URL + __BOOK + 'all')
			get_result = r['result']
			sorted_result = []
			for book in get_result:
				data = book['fields']
				rating = data['rating']
				sorted_result.append((float(rating), data))
			sorted_result = sorted(sorted_result, key = lambda x: x[0], reverse = True)
			sorted_result = sorted_result[0:int(top)]
			returned_list = [data for (rating, data) in sorted_result]
			return __generate_response(top, True, returned_list)

		except Exception as e:
			return __generate_response(str(e), False)


def __make_request(url, data = None, method = 'GET'):
	if data:
		post_encodeda = parse.urlencode(data).encode('utf-8')
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
