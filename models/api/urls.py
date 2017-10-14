from django.conf.urls import url
from api import views, views_author, views_book, views_review

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^author/(?P<author_id>[0-9]+|(all))$', views_author.author, name='author'),
    url(r'^author/create$', views_author.create_author, name='create_author'),
    url(r'^author/delete/(?P<author_id>[0-9]+)$', views_author.delete_author, name='delete_author'),

    url(r'^book/(?P<book_id>[0-9]+|(all))$', views_book.book, name='book'),
    url(r'^book/create$', views_book.create_book, name='create_book'),
    url(r'^book/delete/(?P<book_id>[0-9]+)$', views_book.delete_book, name='delete_book'),

    url(r'^review/(?P<review_id>[0-9]+|(all))$', views_review.review, name='review'),
    url(r'^review/create$', views_review.create_review, name='create_review'),
    url(r'^review/delete/(?P<review_id>[0-9]+)$', views_review.delete_review, name='delete_review'),
]