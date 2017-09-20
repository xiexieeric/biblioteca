from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^hello_world/$', views.hello_world, name='hello'),
    url(r'^author/(?P<author_id>[0-9]+)/$', views.author, name='author'),
    url(r'^book/$', views.hello_world, name='hello'),
    url(r'^review/$', views.hello_world, name='hello')
]