from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.squirl_login, name = 'squirl_login'),
    url(r'^addEvent/$', views.add_event, name = 'addEvent'),
]
