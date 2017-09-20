from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.

def hello_world(request):
	return HttpResponse('Hello World')

def author(request, author_id):
	if request.method == 'GET':
		return HttpResponse('GET ' + author_id)
	if request.method == 'POST':
		return HttpResponse('POST ' +  author_id)
