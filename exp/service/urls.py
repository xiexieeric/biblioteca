from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),

    url(r'^home/$', views.home, name='home'),
    url(r'^book/top/(?P<count>[0-9]+)$', views.get_top_books, name='top_book'),
    url(r'^book/recent/(?P<count>[0-9]+)$', views.get_recent_books, name='recent_book'),

    url(r'^book/(?P<book_id>[0-9]+|(all))$', views.book, name='book'),
    url(r'^author/(?P<author_id>[0-9]+|(all))$', views.author, name='author'),
    url(r'^review/(?P<review_id>[0-9]+|(all))$', views.review, name='review'),
    url(r'^listing/(?P<listing_id>[0-9]+|(all))$', views.listing, name='listing'),
    url(r'^user/(?P<user_id>[0-9]+|(all))$', views.user, name='user'),
    url(r'^authenticator/(?P<auth_id>[0-9a-z]+|(all))$', views.authenticator, name='authenticator'),

    url(r'^listing/create$', views.create_new_listing, name='create_listing'),
    url(r'^listing/click$', views.user_click_listing, name='click_listing'),


    url(r'^signup', views.create_account, name='signup'),
    url(r'^login', views.user_login, name='login'),
    url(r'^logout', views.user_logout, name='logout'),
]