from django.urls import path

from . import views

urlpatterns = [
    path('registrationWorker', views.registrationWorker, name='registrationWorker'),
    path('registrationUser', views.registrationUser, name='registrationUser'),
    path('login', views.login, name='login'),
    path('getall', views.getall, name='getall'),
    path('get_search_results', views.get_search_results, name='get_search_results'),
    path('getProfileInfo', views.getProfileInfo, name='getProfileInfo'),
    path('updateProfileInfoAddress', views.updateProfileInfoAddress,
         name='updateProfileInfoAddress'),
    path('updateProfileInfoWorkingHour', views.updateProfileInfoWorkingHour,
         name='updateProfileInfoWorkingHour'),



]
