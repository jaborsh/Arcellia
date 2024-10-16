"""
This reroutes from an URL to a python view-function/class.

The main web/urls.py includes these routes for all urls (the root of the url)
so it can reroute to all website pages.

"""

from django.urls import path
from evennia.web.website.urls import urlpatterns as evennia_website_urlpatterns

from web.website.views import index

# add patterns here
urlpatterns = [
    path("", index.EvenniaIndexView.as_view(), name="index")
    # path("url-pattern", imported_python_view),
]

# read by Django
urlpatterns = urlpatterns + evennia_website_urlpatterns
