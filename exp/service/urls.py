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
    
    url(r'^signup', views.signup, name='signup'),
]