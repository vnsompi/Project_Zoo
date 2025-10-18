"""
Models for user

"""

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField

class UserManager(BaseUserManager):
    """manager for user model"""

    def create_user(self, email, password, **extra_fields):
        """Create and save a new user"""
        if not email:
            raise ValueError('User must have an email address')

        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a new superuser"""

        user = self.create_user(email, password, **extra_fields)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username"""
    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


"""event's table """

class Event(models.Model):
    """event model"""
    DAYS_OF_WEEK = [
        ('monday', 'Lundi'),
        ('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),
        ('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),
        ('saturday', 'Samedi'),
        ('sunday', 'Dimanche'),
    ]
    title = models.CharField(max_length=255)
    day = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    description = models.TextField()
    Event_date = models.DateField()
    participants = models.ManyToManyField(User, related_name='events')
    price = models.DecimalField(decimal_places=2, max_digits=10)
    start_time = models.TimeField()
    end_time = models.TimeField()

    def __str__(self):
        return f'{self.title} du {self.Event_date}'



class Ticket(models.Model):
    """ticket model"""
    TYPE_BILLET_CHOICES = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),
        ('etudiant', 'Étudiant'),
        ('famille', 'Famille'),
        ('groupe', 'Groupe'),
    ]
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    type_ticket = models.CharField(max_length=10, choices=TYPE_BILLET_CHOICES)
    visit_date = models.CharField(max_length=10, choices = Event.DAYS_OF_WEEK)
    price = models.DecimalField(decimal_places=2, max_digits=10)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        Rate = {
            'standard': 10000,
            'vip': 25000,
            'etudiant': 7000,
            'famille': 18000,
            'groupe': 15000,
        }

        """filled automatically the price according to the rate"""
        if self.type_ticket in Rate and (self.price is None or self.price == 0):
            self.price = Rate[self.type_ticket]

        super().save(*args, **kwargs)

    def __str__(self):
        return f"ticket for {self.visitor.name} on {self.visit_date}"





class Reservation(models.Model):
    """Reservation model"""
    TYPE_CHOICES = [
        ('adulte', 'Adulte'),
        ('enfant', 'Enfant'),
        ('groupe', 'Groupe'),
        ('vip', 'VIP'),
        ('etudiant', 'Étudiant'),
    ]
    visitors = models.ManyToManyField(User, related_name='reservations')
    tickets = models.ManyToManyField(Ticket, related_name='reservations')
    event = models.ForeignKey(Event, related_name='reservations', on_delete=models.CASCADE)
    type_of_reservation = models.CharField(max_length=10, choices=TYPE_CHOICES)
    total_price = models.DecimalField(decimal_places=2, max_digits=10)
    arrival_time = models.TimeField()
    has_booked = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def save(self, *args, **kwargs):

        Rates = {
            'adulte': 2000,
            'enfant': 1000,
            'groupe': 10000,
            'vip': 25000,
            'etudiant': 3000,
            'couple':35000,
        }

        """apply the total_price if the type is known"""

        if self.type_of_reservation in Rates:
            self.total_price = Rates[self.type_of_reservation]

        super().save(*args, **kwargs)

    def __str__(self):
        return f'Reservation of  {self.visitors.count()} visits {self.tickets.count()} tickets'

