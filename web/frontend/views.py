from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
import urllib.request
import urllib.parse
import json
from .forms import *
from elasticsearch import Elasticsearch
from django.views.decorators.csrf import csrf_exempt

__EXP_URL = 'http://exp-api:8000/api/v1/'

def index(request, context = {}):
	if request.COOKIES.get('auth'):
		req = urllib.request.Request(__EXP_URL+'authenticator/'+str(request.COOKIES.get('auth')))
		resp_auth = urllib.request.urlopen(req).read().decode('utf-8')
		resp_auth = json.loads(resp_auth)
		if resp_auth['success']:
			isLoggedIn = True
			del_cookie = False
		else:
			isLoggedIn = False
			del_cookie = True
	else:
		isLoggedIn = False
		del_cookie = False
	req = urllib.request.Request(__EXP_URL+'home')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if context:
		resp['msg']  = context['msg']
	else:
		resp['msg'] = ""
	if isLoggedIn:
		resp['isLoggedIn'] = True
	response = render(request, 'frontend/index.html', resp)
	if del_cookie:
		response.delete_cookie('auth')
	return response

def book_detail(request, book_id):
	req = urllib.request.Request(__EXP_URL +'book/'+book_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if request.COOKIES.get('auth'):
		resp['isLoggedIn'] = True
	if resp["success"] == True:
		context = {
			"title": resp["result"]["fields"]["title"],
			"year": resp["result"]["fields"]["year_published"],
			"rating": resp["result"]["fields"]["rating"],
		}
		req_2 = urllib.request.Request('http://exp-api:8000/api/v1/author/'+str(resp["result"]["fields"]["author"]))
		resp_json_2 = urllib.request.urlopen(req_2).read().decode('utf-8')
		resp_2 = json.loads(resp_json_2)
		context["author_first"] = resp_2["result"]["fields"]["first_name"]
		context["author_last"] = resp_2["result"]["fields"]["last_name"]
		if request.COOKIES.get('auth'):
			context['isLoggedIn'] = True
		return render(request, 'frontend/book_detail.html', context)
	else:
		return redirect('/notfound')

def listing_detail(request, listing_id):
	if request.COOKIES.get('auth'):
		req = urllib.request.Request(__EXP_URL+'authenticator/'+str(request.COOKIES.get('auth')))
		resp_auth = urllib.request.urlopen(req).read().decode('utf-8')
		resp_auth = json.loads(resp_auth)
		if resp_auth['success']:
			isLoggedIn = True
			del_cookie = False
		else:
			isLoggedIn = False
			del_cookie = True
	else:
		isLoggedIn = False
		del_cookie = False
	req = urllib.request.Request(__EXP_URL +'listing/'+listing_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
	if resp["success"] == True:
		context = {
			"book_title": resp["result"]["fields"]["book_title"],
			"price": resp["result"]["fields"]["price"],
		}
		if resp['recs']:
			context['recs'] = resp['recs']
		req_2 = urllib.request.Request('http://exp-api:8000/api/v1/user/'+str(resp["result"]["fields"]["lister"]))
		resp_json_2 = urllib.request.urlopen(req_2).read().decode('utf-8')
		resp_2 = json.loads(resp_json_2)
		context["first_name"] = resp_2["result"]["fields"]["first_name"]
		context["last_name"] = resp_2["result"]["fields"]["last_name"]
		if isLoggedIn:
			context['isLoggedIn'] = True
			post_data = {'user': resp_auth['result']['fields']['user_id'], 'listing': resp['result']['pk']}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request(__EXP_URL+'listing/click', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
		return render(request, 'frontend/listing_detail.html', context)
	else:
		return redirect('/notfound')

def create_book_listing(request):
	if request.method == "POST":
		form = CreateBookForm(request.POST)
		if form.is_valid():
			req = urllib.request.Request(__EXP_URL+'authenticator/'+str(request.COOKIES.get('auth')))
			resp = urllib.request.urlopen(req).read().decode('utf-8')
			resp = json.loads(resp)
			if resp['success']:
				post_data = {
					'authenticator': request.COOKIES.get('auth'),
					'lister': resp["result"]["fields"]["user_id"],
					'book': form.cleaned_data['book'],
					'price': form.cleaned_data['price']
				}
				post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
				req = urllib.request.Request(__EXP_URL+'listing/create', data=post_encoded, method='POST')
				resp_json = urllib.request.urlopen(req).read().decode('utf-8')
				resp_json = json.loads(resp_json)
				if resp_json['success']:
					return render(request, 'frontend/create_book.html', {'form': form, "msg": "Listing created successfully!"})
				else:
					return render(request, 'frontend/create_book.html',
								  {'form': form, "msg": resp_json['msg']})
			else:
				return render(request, 'frontend/create_book.html', {'form': form, "msg": resp['msg']})
	elif request.COOKIES.get('auth'):
		form = CreateBookForm()
		return render(request, 'frontend/create_book.html', {'form': form})
	else:
		return index(request, {'msg': "You must be logged in to create listing"})

def not_found(request):
	return render(request, 'frontend/404.html', {})

@csrf_exempt
def search(request):
	if request.COOKIES.get('auth'):
		req = urllib.request.Request(__EXP_URL+'authenticator/'+str(request.COOKIES.get('auth')))
		resp_auth = urllib.request.urlopen(req).read().decode('utf-8')
		resp_auth = json.loads(resp_auth)
		if resp_auth['success']:
			isLoggedIn = True
		else:
			isLoggedIn = False
	else:
		isLoggedIn = False
	context = {}
	if request.method == 'POST':
		es = Elasticsearch(['es'])
		try:
			results = es.search(index='listing_index', body={'query': {'query_string': {'query': request.POST.get('search_text') }}, 'size': 10})
		except:
			results = {'msg': "You have no listings"}
		if results['hits']:
			results['count'] = len(results['hits']['hits'])
		else:
			results['count'] = 0
		for hit in results['hits']['hits']:
			hit['source'] = hit['_source']
		context['msg'] = results
		isLoggedIn = True
		if isLoggedIn:
			context['isLoggedIn'] = "True"
		response = render(request, 'frontend/search.html', context)
		if not isLoggedIn:
			response.delete_cookie('auth')
		return response
	else:
		if isLoggedIn:
			context['isLoggedIn'] = True
		response = render(request, 'frontend/search.html', context)
		return response

@csrf_exempt
def signup(request):
	if request.method == 'POST':
		form = SignupForm(request.POST)
		if form.is_valid():
			post_data = {
				'username': form.cleaned_data['username'],
				'password': form.cleaned_data['password'],
				'first_name': form.cleaned_data['fname'],
				'last_name': form.cleaned_data['lname'],
			}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request(__EXP_URL+'signup/', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp_json = json.loads(resp_json)
			if resp_json["success"] == 'true':
				return HttpResponseRedirect('/index')
			else:
				return render(request, 'frontend/signup.html', {'form': form, 'msg': resp_json['msg'],})
	else:
		form = SignupForm()
	return render(request, 'frontend/signup.html', {'form': form})

def login(request):
	if request.COOKIES.get("auth"):
		req = urllib.request.Request(__EXP_URL+'authenticator/'+str(request.COOKIES.get('auth')))
		resp = urllib.request.urlopen(req).read().decode('utf-8')
		resp = json.loads(resp)
		if resp['success']:
			return index(request, {"msg": "You're already logged in!"})
		else:
			response = HttpResponseRedirect('/login/')
			response.delete_cookie('auth')
			return response
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if request.COOKIES.get('auth'):
			return render(request, 'frontend/login.html', {'form': form, 'msg': 'you are already logged in!'})
		if form.is_valid():
			post_data = {
				'username': form.cleaned_data['username'],
				'password': form.cleaned_data['password'],
			}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request(__EXP_URL+'login', data=post_encoded, method='POST')
			resp_json = urllib.request.urlopen(req).read().decode('utf-8')
			resp_json = json.loads(resp_json)
			if resp_json["success"]:
				response = HttpResponseRedirect('/')
				response.set_cookie('auth', resp_json["result"]["pk"])
				return response
			else:
				return render(request, 'frontend/login.html', {'form': form, 'msg': resp_json['msg']})
	else:
		form = LoginForm()
		return render(request, 'frontend/login.html', {'form': form})

def logout(request):
	if request.method == 'GET':
		response = HttpResponseRedirect('/')
		response.delete_cookie('auth')
		if request.COOKIES.get('auth'):
			post_data = {
				'authenticator': request.COOKIES.get('auth'),
			}
			post_encoded = urllib.parse.urlencode(post_data).encode('utf-8')
			req = urllib.request.Request(__EXP_URL + 'login', data=post_encoded, method='POST')
			urllib.request.urlopen(req)
		return response
	else:
		return not_found(request)


