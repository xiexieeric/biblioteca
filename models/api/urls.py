from django.conf.urls import url

from . import views

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    # url(r'^author/$', views.author, name='author'),
    url(r'^author/(?P<author_id>[0-9]+|(all))$', views.author, name='author'),
    url(r'^author/create$', views.create_author, name='create_author'),
    url(r'^author/delete/(?P<author_id>[0-9]+)$', views.delete_author, name='delete_author'),

    url(r'^book/(?P<book_id>[0-9]+|(all))$', views.book, name='book'),
    url(r'^book/create$', views.create_book, name='create_book'),
    url(r'^book/delete/(?P<book_id>[0-9]+)$', views.delete_book, name='delete_book'),

    url(r'^review/(?P<review_id>[0-9]+|(all))$', views.review, name='review'),
    url(r'^review/create$', views.create_review, name='create_review'),
    url(r'^review/delete/(?P<review_id>[0-9]+)$', views.delete_review, name='delete_review'),
]