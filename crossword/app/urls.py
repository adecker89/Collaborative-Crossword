from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('app.views',
    url(r'^$', 'home'),
)
