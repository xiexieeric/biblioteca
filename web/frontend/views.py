from django.shortcuts import render
import urllib.request
import urllib.parse
import json

def index(request):
    return render(request, 'frontend/index.html', {})
