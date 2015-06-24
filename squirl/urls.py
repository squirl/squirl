from django.conf.urls import patterns, include, url
from django.contrib import admin
from dajaxice.core import dajaxice_autodiscover, dajaxice_config
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
dajaxice_autodiscover()

urlpatterns = patterns('',
    # Examples:
                       
    # url(r'^$', 'squirl.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^QED/', include('QED.urls')),
    url(dajaxice_config.dajaxice_url, include('dajaxice.urls')),
)
urlpatterns += staticfiles_urlpatterns()
