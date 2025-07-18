from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.utils import timezone
from datetime import timedelta

class CustomUserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Un email est obligatoire.')
        email = self.normalize_email(email)
        extra_fields.pop('username', None)  # ✅ Propre et safe
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    username = None  # Supprimé
    email = models.EmailField(unique=True)

    ROLE_CHOICES = (
        ('PATIENT', 'Patient'),
        ('DOCTOR', 'Médecin'),
        ('ADMIN', 'Administrateur'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='PATIENT')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()  # ✅ branche ton manager ici

    def __str__(self):
        return f"{self.email} ({self.role})"

class Patient(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return f"Patient: {self.user.get_full_name()} ({self.user.email})"

class Medecin(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    specialty = models.CharField(max_length=100)

    def __str__(self):
        return f"Dr. {self.user.get_full_name()} ({self.specialty})"

class RendezVous(models.Model):
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    disponibilite = models.ForeignKey('Disponibilite', on_delete=models.CASCADE, null=True, blank=True)
    date = models.DateTimeField()
    motif = models.TextField()
    notes_medicales = models.TextField(blank=True)
    rappel_envoye = models.BooleanField(default=False)  # ✔️ ton champ est là !

    def __str__(self):
        return f"{self.date} - {self.patient.user.get_full_name()} avec Dr. {self.medecin.user.get_full_name()}"


class Disponibilite(models.Model):
    medecin = models.ForeignKey('Medecin', on_delete=models.CASCADE, related_name='disponibilites')
    date = models.DateTimeField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.medecin} - {self.date} ({'Réservé' if self.is_booked else 'Libre'})"

    class Meta:
        unique_together = ('medecin', 'date')  # Empêche doublons sur le même créneau

JOUR_CHOICES = [
    (0, "Lundi"), (1, "Mardi"), (2, "Mercredi"),
    (3, "Jeudi"), (4, "Vendredi"), (5, "Samedi"), (6, "Dimanche")
]

class PlageHoraire(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    jour = models.IntegerField(choices=JOUR_CHOICES)
    heure_debut = models.TimeField()
    heure_fin = models.TimeField()
    duree_slot = models.DurationField(default=timedelta(minutes=30))

    def __str__(self):
        return f"{self.get_jour_display()} - {self.heure_debut} à {self.heure_fin}"

class Indisponibilite(models.Model):
    medecin = models.ForeignKey(Medecin, on_delete=models.CASCADE)
    date = models.DateField()
    raison = models.CharField(max_length=255, blank=True)
