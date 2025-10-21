# users/models.py
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    """Manager for User model"""

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("L'utilisateur doit avoir une adresse email")

        extra_fields.setdefault("role", "Visiteur")
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        """create superuser"""
        extra_fields.setdefault("role", "Admin")
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """User  model """
    ROLE_CHOICES = [
        ("Visiteur", "Visiteur"),
        ("Personel", "personel")
    ]


    name = models.CharField(max_length=255)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = PhoneNumberField(unique=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.name} ({self.role})"


    @property
    def is_personnel(self):
        """this function returns True if the user is a personnel"""
        return self.role == "Personnel"


class Personnel(models.Model):
    DEPARTMENT_CHOICES = [
        ('soins_animaux', 'Soins animaux'),('veterinaire', 'Vétérinaire'),
        ('visites', 'Visites guidées'),('maintenance', 'Maintenance'),
        ('administration', 'Administration'),('securite', 'Sécurité'),
        ('accueil', 'Accueil'),('finances', 'Finances'),
        ('communication', 'Communication'),('recherche', 'Recherche'),
        ('restauration', 'Restauration'),('nettoyage', 'Nettoyage'),
        ('informatique', 'Informatique'),('logistique', 'Logistique'),
        ('gestion_animaux', 'Gestion des animaux'),
    ]
    ROLE_CHOICES = [
        ('veterinaire', 'Vétérinaire'),
        ('responsable_soigneurs', 'Responsable soigneurs'),
        ('soigneur', 'Soigneur'),
        ('responsable_accueil', 'Responsable accueil'),
        ('guide_touristique', 'Guide touristique'),
        ('technicien_maintenance', 'Technicien maintenance'),
    ]

    STATUS_CHOICES = [
        ('actif', 'Actif'),
        ('inactif', 'Inactif'),
        ('suspendu', 'Suspendu'),
        ('en_congé', 'En congé'),
        ('en_mission', 'En mission'),
        ('retiré', 'Retiré'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='personnel_profile')
    title = models.CharField(max_length=100)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    department = models.CharField(max_length=50, choices=DEPARTMENT_CHOICES)
    hire_date = models.DateField()
    status = models.CharField(max_length=50, default='active')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.name} - {self.title} ({self.department})"





"""event's table """

class Event(models.Model):
    """event model"""
    DAYS_OF_WEEK = [
        ('monday', 'Lundi'),('tuesday', 'Mardi'),
        ('wednesday', 'Mercredi'),('thursday', 'Jeudi'),
        ('friday', 'Vendredi'),('saturday', 'Samedi'),
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

"""ticket's table """

class Ticket(models.Model):
    """ticket model"""
    TYPE_BILLET_CHOICES = [
        ('standard', 'Standard'),
        ('vip', 'VIP'),('etudiant', 'Étudiant'),
        ('famille', 'Famille'), ('groupe', 'Groupe'),
    ]
    CATEGORIES_CHOICES = [
        ('national', 'National'),
        ('expatrie', 'Expatrié'),
        ('diplomatique', 'Diplomatique'),
    ]

    STATUS_CHOICES = [
        ('valide', 'Valide'),
        ('annule', 'Annulé'),
        ('en_attente', 'En attente'),
    ]

    reference = models.CharField(max_length=50, unique=True)
    visitor = models.ForeignKey(User, on_delete=models.CASCADE)
    type_ticket = models.CharField(max_length=10, choices=TYPE_BILLET_CHOICES)
    category = models.CharField(max_length=15, choices=CATEGORIES_CHOICES)
    visit_date = models.CharField(max_length=10, choices = Event.DAYS_OF_WEEK)
    quantity = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    status = models.CharField(max_length=10, choices = STATUS_CHOICES)
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


"""reservation's table """

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


"""announcement's table """

class Announcement(models.Model):
    """Announcement model"""
    TYPE_CHOICES = [
        ('Published', 'Published'),
        ('Draft','draft')
    ]

    MESSAGE_STATUS_CHOICES = [
        ('Important', 'Important'),
        ('Pertinant', 'Pertinant'),
        ('Urgent', 'Urgent'),
    ]
    title = models.CharField(max_length=255)
    content = models.TextField()
    status = models.CharField(max_length=10, choices=TYPE_CHOICES)
    created_by = models.ForeignKey(User, related_name='announcements', on_delete=models.CASCADE)
    messages = models.CharField(max_length=255, choices=MESSAGE_STATUS_CHOICES)
    begin_date = models.DateField()
    end_date = models.DateField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.title} on {self.begin_date}  to {self.end_date} '


"""sale's table """

class Sale(models.Model):
    """Sale model"""
    TYPE_CHOICES = [
        ('USD','usd'),
        ('CDF','cdf')
    ]

    client_name = models.ForeignKey(User, related_name='sales', on_delete=models.CASCADE)
    total_revenue = models.DecimalField(decimal_places=2, max_digits=10)
    total_paid =  models.DecimalField(decimal_places=2, max_digits=10)
    primary_currency = models.CharField(max_length=10, choices=TYPE_CHOICES)
    date = models.DateField()

    def __str__(self):
        return f'{self.client_name} on {self.date}'




class Animal(models.Model):
    """Annotation model"""
    SPECIES_CHOICES = [
        ('chien', 'Chien'),('chat', 'Chat'),('lapin', 'Lapin'),('cheval', 'Cheval'),('vache', 'Vache'),
        ('cochon', 'Cochon'),('chevre', 'Chèvre'),('mouton', 'Mouton'),('poule', 'Poule'),('lion', 'Lion'),
        ('tigre', 'Tigre'),('elephant', 'Éléphant'),('girafe', 'Girafe'),('zebre', 'Zèbre'),('gorille', 'Gorille'),
        ('chimpanze', 'Chimpanzé'),('panda', 'Panda'),('ours_polaire', 'Ours polaire'),('leopard', 'Léopard'),
        ('rhinoceros', 'Rhinocéros'),('hippopotame', 'Hippopotame'),('crocodile', 'Crocodile'),
        ('lama', 'Lama'),('autruche', 'Autruche'),('pelican', 'Pélican'),('flamant_rose', 'Flamant rose'),
        ('serpent', 'Serpent'),('tortue_geante', 'Tortue géante'),('kangourou', 'Kangourou'),
    ]

    HEALTH_STATUS_CHOICES = [
        ('bon', 'Bon'),
        ('moyen', 'Moyen'),
        ('critique', 'Critique'),
        ('en_traitement', 'En traitement'),
        ('modéré', 'Modéré')
    ]

    CARETAKER_CHOICES = [
    ('jean_kabasela', 'Jean Kabasela'),
    ('marie_lumbala', 'Marie Lumbala'),
    ('paul_mbayo', 'Paul Mbayo'),
    ('sophie_nkosi', 'Sophie Nkosi'),
    ]

    name = models.CharField(max_length=255)
    age = models.IntegerField()
    species = models.CharField(max_length=255, choices=SPECIES_CHOICES)
    enclosure = models.CharField(max_length=255)
    caretaker = models.CharField(max_length=255, choices =CARETAKER_CHOICES )
    health_status = models.CharField(max_length=255, choices=HEALTH_STATUS_CHOICES)
    is_being_treated = models.BooleanField(default=False)
    last_control = models.DateTimeField()


    def __str__(self):
        return f'{self.name} of {self.enclosure}'




class ZooParams(models.Model):
    """ZooParams model"""

    TYPE_CHOICES = [
        ('USD', 'usd'),
        ('CDF', 'cdf')
    ]
    LANGUE_CHOICES = [
        ('Français', 'fr'),('Anglais', 'en'),('Espagnol', 'es'),
        ('Portugais', 'pt'),('Allemand', 'de'),('Italien', 'it'),
        ('Chinois', 'zh'),('Japonais', 'ja'),('Coréen', 'ko'),
        ('Arabe', 'ar'),('Russe', 'ru'),('Swahili', 'sw'),
        ('Lingala', 'ln'),('Kikongo', 'kg'),('Haoussa', 'ha'),
    ]

    name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    phone = PhoneNumberField(unique=True)
    currency = models.CharField(max_length=12, choices=TYPE_CHOICES)
    address = models.CharField(max_length=255)
    language = models.CharField(max_length=255, choices=LANGUE_CHOICES)
    format_date = models.DateField()

    def __str__(self):
        return f' Parameter of : {self.name} at : {self.address}'





















