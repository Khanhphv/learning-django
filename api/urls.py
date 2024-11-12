from django.urls import path

from api import views

urlpatterns = [
    path('/login', views.login),
    # path('logout', views.logout),
    # path('register', views.register),
    path('/users', views.user_list),
]
