from django.conf.urls import url

from everecon.navigate import views

urlpatterns = [
    url(r'^systems/', views.get_systems),
    url(r'^around/', views.around, name='around'),
    url(r'^live/', views.live, name='live'),
    url(r'^sigma/data', views.sigma_json),
    url(r'^sigma/', views.sigma, name='sigma')

]
