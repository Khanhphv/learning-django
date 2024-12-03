from django.urls import path

from api_auth import views

urlpatterns = [
    path('login', views.login),
    # path('logout/', views.logout, name='logout'),
    # path('refresh-token/', views.refresh_token, name='refresh_token'),
    path('user-list', views.user_list),
]
