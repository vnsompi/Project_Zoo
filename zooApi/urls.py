"""
urls for user
"""
from django.urls import path
from zooApi import views


app_name = 'zooApi'

urlpatterns = [
    path('events/',views.EventListCreateView.as_view(), name='event_list'),
    path('event/<int:pk>/',views.EventDetailView.as_view(), name='event_detail'),
    path('reservations/',views.ReservationListView.as_view(), name='reservation'),
    path('reservation/<int:pk>/',views.ReservationDetailView.as_view(), name='reservation_detail'),
    path('register/user/', views.CreateUserView.as_view(), name='create'),
    path('token/', views.CreateTokenView.as_view(), name='token'),
    path('tickets',views.TicketListCreateView.as_view(), name='ticket_list'),
    path('ticket/<int:pk>/',views.TicketDetailView.as_view(), name='ticket_detail'),
    path('user/profile/', views.ManageUserView.as_view(), name='me'),
]
