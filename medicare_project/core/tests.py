from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, Patient, Medecin, RendezVous


class RendezVousTests(APITestCase):
    def setUp(self):
        # Crée un Patient
        self.patient_user = User.objects.create_user(
            username="testpatient",
            password="Patient123.",
            role="PATIENT"
        )
        self.patient_profile = Patient.objects.create(
            user=self.patient_user,
            phone="0600000000"
        )

        # Crée un Médecin
        self.doctor_user = User.objects.create_user(
            username="testdoctor",
            password="Doctor123.",
            role="DOCTOR"
        )
        self.doctor_profile = Medecin.objects.create(
            user=self.doctor_user,
            specialty="Cardiologie"
        )

        # Crée un Admin
        self.admin_user = User.objects.create_user(
            username="testadmin",
            password="Admin123.",
            role="ADMIN"
        )

        # Génère les tokens JWT
        self.patient_token = RefreshToken.for_user(self.patient_user).access_token
        self.doctor_token = RefreshToken.for_user(self.doctor_user).access_token
        self.admin_token = RefreshToken.for_user(self.admin_user).access_token

    def test_patient_can_create_rendezvous(self):
        # Authentifie en tant que Patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patient_token}')

        url = reverse('rendezvous-list')  # /api/rendezvous/
        data = {
            "medecin": self.doctor_profile.id,
            "date": "2025-07-31T10:00:00Z",
            "motif": "Test par patient"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RendezVous.objects.count(), 1)
        self.assertEqual(RendezVous.objects.first().patient, self.patient_profile)

    def test_doctor_cannot_create_rendezvous(self):
        # Authentifie en tant que Médecin
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.doctor_token}')

        url = reverse('rendezvous-list')
        data = {
            "medecin": self.doctor_profile.id,
            "date": "2025-07-31T11:00:00Z",
            "motif": "Test par médecin"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(RendezVous.objects.count(), 0)

    def test_admin_can_create_rendezvous(self):
        # Authentifie en tant qu'Admin
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.admin_token}')

        url = reverse('rendezvous-list')
        data = {
            "patient": self.patient_profile.id,
            "medecin": self.doctor_profile.id,
            "date": "2025-07-31T12:00:00Z",
            "motif": "Test par admin"
        }

        response = self.client.post(url, data, format='json')

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(RendezVous.objects.count(), 1)
        self.assertEqual(RendezVous.objects.first().patient, self.patient_profile)

    def test_patient_list_only_own_rendezvous(self):
        # Crée un rendez-vous pour le Patient
        RendezVous.objects.create(
            patient=self.patient_profile,
            medecin=self.doctor_profile,
            date="2025-07-31T14:00:00Z",
            motif="Consultation test"
        )

        # Authentifie en tant que Patient
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {self.patient_token}')

        url = reverse('rendezvous-list')
        response = self.client.get(url, format='json')

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

class RegisterTests(APITestCase):
    def test_register_patient_success(self):
        url = reverse('register')
        data = {
            "username": "axel",
            "email": "axel@example.com",
            "password": "TestPass123.",
            "role": "PATIENT"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="axel").exists())
        self.assertTrue(Patient.objects.filter(user__username="axel").exists())
        self.assertEqual(User.objects.get(username="axel").role, "PATIENT")

    def test_register_doctor_success(self):
        url = reverse('register')
        data = {
            "username": "drbob",
            "email": "bob@example.com",
            "password": "SuperPass456.",
            "role": "DOCTOR"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertTrue(User.objects.filter(username="drbob").exists())
        self.assertTrue(Medecin.objects.filter(user__username="drbob").exists())
        self.assertEqual(User.objects.get(username="drbob").role, "DOCTOR")

    def test_register_invalid_role(self):
        url = reverse('register')
        data = {
            "username": "vilain",
            "email": "vilain@example.com",
            "password": "vilainPass123.",
            "role": "HACKER"
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertFalse(User.objects.filter(username="vilain").exists())
