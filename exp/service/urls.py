from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^home/$', views.home, name='home'),
    url(r'^book/top/(?P<count>[0-9]+)$', views.get_top_books, name='top_book'),
    url(r'^book/recent/(?P<count>[0-9]+)$', views.get_recent_books, name='recent_book'),
    # url(r'^author/create$', views.create_author, name='create_author'),
    # url(r'^author/delete/(?P<author_id>[0-9]+)$', views.delete_author, name='author'),
]