from django.conf.urls import url

from everecon.navigate import views

urlpatterns = [
    url(r'^systems/', views.get_systems),
    url(r'^around/', views.around, name='around')
]
