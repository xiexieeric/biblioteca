from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import csrf_exempt

from json import loads, dumps
from django.core import serializers

"""
Contains base functions common to all views.
"""
def index(request):
	return HttpResponse('Welcome to the index page for API v1')


def serialize(obj):
	"""
	Easy json serialization for a single object.
	"""
	serialized = serializers.serialize('json', [obj])
	data = loads(serialized)
	return data[0] # Cuts off the first and last char '[' and ']' to match assignment format.


def generate_response(msg, success, obj=None, obj_list=None, payload=None):
	res = {}
	res["success"] = success
	res["msg"] = msg
	if obj: res["result"] = serialize(obj)
	elif obj_list:
		json_list = []
		for entry in obj_list:
			json_list.append(serialize(entry))
		res["result"] = json_list
	elif payload:
		for key in payload:
			res[key] = payload[key]
	return JsonResponse(res)











