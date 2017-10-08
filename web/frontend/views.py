from django.shortcuts import render, redirect
import urllib.request
import urllib.parse
import json

def index(request):
	req = urllib.request.Request('http://exp-api:8000/api/v1/home')
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)

	return render(request, 'frontend/index.html', resp)

def book_detail(request, book_id):
	req = urllib.request.Request('http://exp-api:8000/api/v1/book/'+book_id)
	resp_json = urllib.request.urlopen(req).read().decode('utf-8')
	resp = json.loads(resp_json)
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
		return render(request, 'frontend/detail.html', context)
	else:
		return redirect('/notfound')

def not_found(request):
	return render(request, 'frontend/404.html', {})
