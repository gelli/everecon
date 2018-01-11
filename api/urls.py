from django.conf.urls import url

from api import views

urlpatterns = [
    url(r'^systems/', views.get_systems)
]
