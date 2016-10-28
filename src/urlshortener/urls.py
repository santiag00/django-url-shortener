from django.conf.urls import url, include
from api import views

urlpatterns = [
    url(r'^api/', include('api.urls')),
    url(r'^(?P<url>.+)/$', views.redirect_url),
]
