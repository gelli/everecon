from django.conf.urls import url

from everecon.sso import views

urlpatterns = [
    url(r'^login', views.sso_login, name='login'),
    url(r'^callback', views.callback),
    url(r'^logout', views.sso_logout, name='logout')
]
