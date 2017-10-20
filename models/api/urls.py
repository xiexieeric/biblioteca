from django.conf.urls import url
from api import views, views_author, views_book, views_review, views_user, views_authenticator

app_name = 'api'
urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^user/authenticate$', views_user.authenticate_user, name='authenticate_user'),
    url(r'^user/create$', views_user.create_user, name='create_user'),

    url(r'^authenticator$', views_authenticator.authenticator, name='authenticator'),

    url(r'^author/(?P<author_id>[0-9]+|(all))$', views_author.author, name='author'),
    url(r'^author/create$', views_author.create_author, name='create_author'),
    url(r'^author/delete/(?P<author_id>[0-9]+)$', views_author.delete_author, name='delete_author'),

    url(r'^book/(?P<book_id>[0-9]+|(all))$', views_book.book, name='book'),
    url(r'^book/create$', views_book.create_book, name='create_book'),
    url(r'^book/delete/(?P<book_id>[0-9]+)$', views_book.delete_book, name='delete_book'),

    url(r'^review/(?P<review_id>[0-9]+|(all))$', views_review.review, name='review'),
    url(r'^review/create$', views_review.create_review, name='create_review'),
    url(r'^review/delete/(?P<review_id>[0-9]+)$', views_review.delete_review, name='delete_review'),

    url(r'^listing/(?P<listing_id>[0-9]+|(all))$', views_listing.listing, name='listing'),
    url(r'^listing/create$', views_listing.create_listing, name='create_listing'),
    url(r'^listing/delete/(?P<listing_id>[0-9]+)$', views_listing.delete_listing, name='delete_listing'),
]