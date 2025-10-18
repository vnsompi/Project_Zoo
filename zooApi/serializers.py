"""
serializers for users
"""

from rest_framework import serializers
from django.contrib.auth import get_user_model,authenticate
from django.utils.translation import gettext_lazy as _
from zooApi import models



class UserSerializer(serializers.ModelSerializer):
    """serializer for user model"""
    class Meta:
        model = get_user_model()
        fields = ['name','email','phone_number','password','is_active']
        extra_kwargs = {'password': {'write_only': True, 'min_length': 5}}

    def create(self, validated_data):
        """create and return a new `User` instance, given the validated data"""
        return get_user_model().objects.create_user(**validated_data)

    def update(self, instance, validated_data):
        """update and return user with entered data"""
        password = validated_data.pop('password', None)
        user = super().update(instance, validated_data)

        if password:
            user.set_password(password)
            user.save()
        return user


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
        """read_only_fields = ('visitors', 'type_of_reservation')"""





















