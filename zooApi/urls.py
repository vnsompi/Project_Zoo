"""
urls for user
"""
from django.urls import path
from zooApi import views
from zooApi.views import AdminProfileView

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
    path('user/profiles/admin/', AdminProfileView.as_view(), name='admin-profiles'),
    path('parameters/zoo', views.ZooParamsListCreateView.as_view(), name='zoo-params'),

    path('animals/',views.AnimalListCreateView.as_view(), name='animal-list'),
    path('animal/<int:pk>/',views.AnimalDetailView.as_view(), name='animal-list'),

    path('sales/',views.SalesListCreateView.as_view(), name='sales-list'),
    path('sale/<int:pk>/',views.SalesDetailView.as_view(), name='sales-detail'),

    path('announcements/',views.AnnouncementListCreateView.as_view(), name='announcement-list'),
    path('announcement/<int:pk>/', views.AnnouncementDetailView.as_view(), name='announcement-detail'),

    path('personnels/', views.PersonnelListCreateView.as_view(), name='personnel-list'),
    path('personnel/<int:pk>/',views.PersonnelDetailView.as_view(), name='person-list'),
]
