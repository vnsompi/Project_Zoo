"""
Serializers for users
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext_lazy as _
from zooApi import models

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Serializer for th standard user """

    class Meta:
        model = User
        fields = [
            'id', 'name',
            'email', 'phone_number',
            'password', 'role',
            'is_active', 'date_joined',
        ]

        read_only_fields = ['id', 'role', 'is_active', 'date_joined']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """Create a new user which has role in default"""

        return User.objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update a user """


        password = validated_data.pop('password', None)
        validated_data.pop('role', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


class AdminUserSerializer(serializers.ModelSerializer):

    department = serializers.CharField(source='personnel_profile.department', read_only=True)
    hire_date = serializers.DateField(source='personnel_profile.hire_date', read_only=True)
    title = serializers.CharField(source='personnel_profile.title', read_only=True)
    role_personnel = serializers.CharField(source='personnel_profile.role', read_only=True)
    status = serializers.CharField(source='personnel_profile.status', read_only=True)

    class Meta:
        model = User
        fields = [
            'id','name','email','phone_number','role',
            'department','hire_date','title','role_personnel','status',
            'is_active','is_staff','date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for authenticating requests with"""
    email = serializers.CharField()
    password = serializers.CharField(
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    def validate(self, attrs):
        """Validate and authenticate request"""
        email = attrs.get('email')
        password = attrs.get('password')

        user = authenticate(
            request=self.context.get('request'),
            username=email,
            password=password
        )

        if not user:
            msg = _('Impossible de s’authentifier avec les identifiants fournis')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs



class EventSerializer(serializers.ModelSerializer):
    """serializer for event model"""

    class Meta:
        model = models.Event
        fields = ['id','title','description','Event_date','participants','price','start_time','end_time']




class ReservationSerializer(serializers.ModelSerializer):
    """serializer for reservation model"""

    class Meta:
        model = models.Reservation
        fields = ['id','visitors',
                  'tickets','event',
                  'type_of_reservation',
                  'total_price','arrival_time',
                  'has_booked','created_at',
                  'updated_at']

        """   read_only_fields = ('visitors', 'type_of_reservation')  """



class TicketSerializer(serializers.ModelSerializer):
    """serializer for ticket model"""
    class Meta:
        model = models.Ticket
        fields = ['id','reference','visitor','type_ticket','category','visit_date',
                  'quantity','price','status','created_at']




class AnnouncementSerializer(serializers.ModelSerializer):
    """serializer for announcement model"""
    class Meta:
        model = models.Announcement
        fields = ['id','title','content','status','created_by',
                  'created_at','messages','begin_date', 'end_date', ]


class SaleSerializer(serializers.ModelSerializer):
    """serializer for sale model"""
    class Meta:
        model = models.Sale
        fields = ['id','client_name', 'total_revenue', 'total_paid',
                 'primary_currency', 'date' ]


class AnimalSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Animal
        fields = [
            'id','name',
            'age','species',
            'enclosure','caretaker',
            'health_status','is_being_treated',
            'last_control',
        ]



class ZooParamsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.ZooParams
        fields = [
            'id','name',
            'email','phone',
            'currency','address',
            'language','format_date',
        ]




"""for personel"""

class PersonnelSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = models.Personnel
        fields = ['id', 'user', 'title', 'role','department', 'hire_date',
                  'status','created_at', 'updated_at']