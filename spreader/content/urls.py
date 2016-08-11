from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^getpost/$', views.get_post, name='getpost'),
    url(r'^next/(?P<poolentry_unique_id>.{64})/$', views.get_next, name='getnext'),
    url(r'^spread/(?P<poolentry_unique_id>.{64})/$', views.spread_it, name='spreadit'),
    url(r'^submitcomment/(?P<poolentry_unique_id>.{64})/$', views.submit_comment, name='submitcomment'),
    url(r'^perma/(?P<post_pk>\d+)/$', views.perma_post, name='permapost'),
]
