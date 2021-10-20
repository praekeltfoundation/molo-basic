from django.conf.urls import include, url
from django.views.decorators.cache import never_cache

from wagtail.utils.urlpatterns import decorate_urlpatterns
from wagtail.images.views.serve import ServeView

from .api.urls import api_router
from . import views


urlpatterns = [
    url(
        r'^images/([^/]*)/(\d*)/([^/]*)/[^/]*$',
        ServeView.as_view(),
        name='wagtailimages_serve'
    ),
    url(r'^search/$', views.search, name='search'),
    url(
        r'^locale/(?P<locale>[\w\-\_]+)/$',
        views.locale_set,
        name='locale_set'
    ),
    url(
        r'^health/$',
        views.health,
        name='health'
    ),
    url(
        r'^home-index/$',
        views.home_index,
        name='home_index'
    ),
    url(
        r'^section-index/$',
        views.section_index,
        name='section_index'
    ),
    url(
        r'^search-index/$',
        views.search_index,
        name='search_index'
    ),
    url(
        r'^home-more/$',
        views.home_more,
        name='home_more'
    ),
    url(
        r'^versions/$',
        views.versions,
        name='versions'),
    url(r'^djga/', include('google_analytics.urls')),
    url(r'^(\d+)/publish/$', views.publish, name='publish'),
    url(
        r'^(\d+)/copy_to_all_confirm/$',
        views.copy_to_all_confirm, name='copy-to-all-confirm'),
    url(
        r'^(\d+)/copy_to_all/$',
        views.copy_to_all, name='copy-to-all'),
    url('', include('django_prometheus.urls')),
]
