"""
Views for user management
"""

from rest_framework import generics, permissions, authentication
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from django.contrib.auth import get_user_model
from .models import( Event, Reservation, Ticket, Announcement, Sale, Animal,
                     ZooParams,Personnel)
from .permissions import IsAdminOrReadOnly, IsAdminUserCustom

from .serializers import (

    UserSerializer,
    AuthTokenSerializer,
    AdminUserSerializer,
    EventSerializer,
    ReservationSerializer,
    TicketSerializer, AnnouncementSerializer, SaleSerializer,
    AnimalSerializer, ZooParamsSerializer,PersonnelSerializer
)



User = get_user_model()



class CreateUserView(generics.CreateAPIView):
    """Create a new user (default role = visitor)"""
    serializer_class = UserSerializer




class AdminProfileView(generics.ListCreateAPIView, generics.RetrieveUpdateDestroyAPIView):

    serializer_class = AdminUserSerializer
    queryset = User.objects.filter(is_staff=True)
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]

    def get_queryset(self):
        """Limit results to admin users only"""
        return User.objects.filter(is_staff=True)



class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for a user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Retrieve or update the authenticated user profile"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_serializer_class(self):
        """Use a different serializer if user is admin"""
        user = self.request.user
        if user.is_staff or user.is_superuser:
            return AdminUserSerializer
        return UserSerializer

    def get_object(self):
        """Retrieve and return the authenticated user"""
        return self.request.user




class EventListCreateView(generics.ListCreateAPIView):
    """get the list or create a new event """
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]



class EventDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete event"""
    queryset = Event.objects.all()
    serializer_class = EventSerializer
    permission_classes = [IsAdminOrReadOnly]



class ReservationListView(generics.ListCreateAPIView):
    """get the list of reservations """
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class ReservationDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete reservation"""
    queryset = Reservation.objects.all()
    serializer_class = ReservationSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]


class TicketListCreateView(generics.ListCreateAPIView):
    """get the list of tickets """
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete ticket"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrReadOnly]



class  AnnouncementListCreateView(generics.ListCreateAPIView):
    """create and get the list of announcements """

    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]


class   AnnouncementDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete announcement"""
    queryset = Announcement.objects.all()
    serializer_class = AnnouncementSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]




class SalesListCreateView(generics.ListCreateAPIView):
    """create and get  the list of sales """
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]


class SalesDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete sales"""
    queryset = Sale.objects.all()
    serializer_class = SaleSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]


class AnimalListCreateView(generics.ListCreateAPIView):
    """create and get the list of animals in the system """
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]

class AnimalDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete animal"""
    queryset = Animal.objects.all()
    serializer_class = AnimalSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]


class ZooParamsListCreateView(generics.ListCreateAPIView):
    """create and get the list of zoo params in the system """
    queryset = ZooParams.objects.all()
    serializer_class = ZooParamsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]


"""class ZooParamsDetailView(generics.RetrieveUpdateDestroyAPIView):
    retrieve, update and delete zoo params
    queryset = ZooParams.objects.all()
    serializer_class = ZooParamsSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]
    """



class PersonnelListCreateView(generics.ListCreateAPIView):
    """create and get the list of personnel in the system """
    queryset = Personnel.objects.select_related('user').all()
    serializer_class = PersonnelSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]


class PersonnelDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve and delete  in the system """
    queryset = Personnel.objects.select_related('user').all()
    serializer_class = PersonnelSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminUserCustom]







