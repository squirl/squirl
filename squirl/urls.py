from django.conf.urls import url

from . import views
from . import ajaxViews
urlpatterns = [
    url(r'^$', views.index, name = 'index'),
    url(r'^login/$', views.squirl_login, name = 'squirl_login'),
    url(r'^addEvent/$', views.add_event, name = 'addEvent'),
    url(r'^signOut/$', views.squirl_logout, name='squirl_logout'),
    url(r'^createGroup/$', views.create_group, name='createGroup'),
    url(r'^event/(?P<event_id>[0-9]+)/$',views.event_page, name='event_page'),
    url(r'^group/(?P<group_id>[-\w ]+)/$',views.group_page, name='group_page'),
    url(r'^createAccount/$', views.create_account, name='create_account'),
    url(r'^search/$', views.search_page, name='search_page'),
    url(r'^profile/(?P<user_id>[0-9]+)/$', views.profile_page, name='profile_page'),
    url(r'^joinGroup/(?P<group_id>[\w ]+)/$', views.join_group_request, name='join_group_request'),
    url(r'^subGroupRequest/$', ajaxViews.handle_sub_group_request, name='handle_sub_group_request'),
    url(r'^editEvent/(?P<event_id>[0-9]+)/$',views.edit_event, name='edit_event'),
    url(r'^searchSubmit/$', ajaxViews.search_page, name='search_page'),
]
