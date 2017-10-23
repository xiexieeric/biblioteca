from django.conf.urls import url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static

from . import views

app_name = 'frontend'
urlpatterns = [
	url(r'^$', views.index, name="index"),
	url(r'^book/(?P<book_id>[0-9]+|(all))$', views.book_detail, name='book_detail'),
	url(r'^notfound/', views.not_found, name='not_found'),
	url(r'^signup/', views.signup, name='signup'),
	url(r'^login/', views.login, name='login'),
	url(r'^logout/', views.logout, name='logout'),
	url(r'^create/book', views.create_book_listing, name='create_book'),
] 
