"""
view for user
"""


from rest_framework import generics, permissions, authentication
from rest_framework.settings import api_settings
from rest_framework.authtoken.views import ObtainAuthToken
from .models import Event, Reservation, Ticket
from .serializers import UserSerializer, AuthTokenSerializer, EventSerializer, ReservationSerializer, TicketSerializer
from .permissions import IsAdminOrReadOnly


class CreateUserView(generics.CreateAPIView):
    """Create a new user in the system"""
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """Create a new auth token for user"""
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """Manage the authenticated user retrieving and updating user profile"""
    serializer_class = UserSerializer
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Retrieve and return authenticated user"""
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
    permission_classes = [IsAdminOrReadOnly]


class TicketDetailView(generics.RetrieveUpdateDestroyAPIView):
    """retrieve, update and delete ticket"""
    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = [IsAdminOrReadOnly]









