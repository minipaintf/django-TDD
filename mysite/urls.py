from django.conf.urls import patterns, include, url
from django.contrib import admin
from polls.views import home
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'mysite.views.home', name='home'),
    # url(r'^mysite/', include('mysite.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
                       url(r'^$', home),
                       url(r'^admin/', include(admin.site.urls)),
                       url(r'^poll/(\d+)/$', 'polls.views.poll'),
)
