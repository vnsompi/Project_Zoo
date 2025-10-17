"""
urls for user
"""
from django.urls import path
from zooApi import views


app_name = 'zooApi'

urlpatterns = [
    path('register/user', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('user/profile/', views.ManageUserView.as_view(), name='me'),
]
