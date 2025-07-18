from rest_framework import viewsets, status, generics, serializers
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, IsAuthenticatedOrReadOnly,AllowAny
from rest_framework.exceptions import PermissionDenied
from .models import Patient, Medecin, RendezVous, Disponibilite, PlageHoraire
from .serializers import PatientSerializer, MedecinSerializer, RendezVousSerializer, RegisterSerializer, PatientProfileUpdateSerializer, MedecinProfileUpdateSerializer, DisponibiliteSerializer, CustomTokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
from datetime import datetime, timedelta
from rest_framework.views import APIView


class RendezVousViewSet(viewsets.ModelViewSet):
    queryset = RendezVous.objects.all()
    serializer_class = RendezVousSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
    
        if user.role == 'PATIENT':
            return RendezVous.objects.filter(patient__user=user)
    
        elif user.role == 'DOCTOR':
            return RendezVous.objects.filter(medecin__user=user)
    
        elif user.role == 'ADMIN':
            return RendezVous.objects.all()
    
        return RendezVous.objects.none()


    def perform_create(self, serializer):
        user = self.request.user

        if user.role == 'PATIENT':
            patient_profile = getattr(user, 'patient', None)
            if not patient_profile:
                raise PermissionDenied("Profil patient introuvable.")

            dispo = serializer.validated_data.get('disponibilite')
            if not dispo:
                raise serializers.ValidationError("Un créneau disponible est requis.")

            # ✅ Fixe la date depuis le créneau
            rendezvous = serializer.save(
                patient=patient_profile,
            medecin=dispo.medecin,
            date=dispo.date
        )

        dispo.is_booked = True
        dispo.save()

        # ✅ Email de confirmation
        send_mail(
            subject="Confirmation de votre rendez-vous",
            message=(
                f"Bonjour {user.first_name},\n\n"
                f"Votre rendez-vous est confirmé pour le {rendezvous.date}.\n"
                f"Motif : {rendezvous.motif}\n\n"
                "Merci pour votre confiance.\nL'équipe MediCare."
            ),
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            html_message=(
                f"<h2>Bonjour {user.first_name},</h2>"
                f"<p>Votre rendez-vous est confirmé pour le <strong>{rendezvous.date}</strong>.</p>"
                f"<p><strong>Motif :</strong> {rendezvous.motif}</p>"
                "<p>Merci pour votre confiance.<br>L'équipe MediCare.</p>"
            )
        )

        if user.role == 'PATIENT':
            try:
                patient_profile = user.patient
            except:
                raise PermissionDenied("Profil patient introuvable.")

            rendezvous = serializer.save(patient=patient_profile)

            if hasattr(rendezvous, 'disponibilite'):
                dispo = rendezvous.disponibilite
                dispo.is_booked = True
                dispo.save()
            else:
                raise PermissionDenied("Seuls les patients doivent choisir une disponibilité.")

        elif user.role == 'DOCTOR':
            raise PermissionDenied("Les médecins ne peuvent pas créer de rendez-vous ici.")

        elif user.role == 'ADMIN':
            serializer.save()

        else:
            raise PermissionDenied("Rôle non autorisé.")

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.disponibilite:
            instance.disponibilite.is_booked = False
            instance.disponibilite.save()
        self.perform_destroy(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
    
    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        user = request.user

        # ✅ Vérifie si c'est le bon docteur
        if user.role == 'DOCTOR' and instance.medecin.user != user:
            raise PermissionDenied("Vous ne pouvez modifier que vos propres rendez-vous.")

        # ✅ Autorise PATCH uniquement de notes_medicales
        if user.role == 'DOCTOR':
            notes = request.data.get('notes_medicales')
            if notes is not None:
                instance.notes_medicales = notes
                instance.save()
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
            else:
                return Response({"detail": "Veuillez fournir notes_medicales."}, status=status.HTTP_400_BAD_REQUEST)

        return super().update(request, *args, **kwargs)

class PatientViewSet(viewsets.ModelViewSet):
    queryset = Patient.objects.all()
    serializer_class = PatientSerializer
    permission_classes = [IsAdminUser]


class MedecinViewSet(viewsets.ModelViewSet):
    queryset = Medecin.objects.all()
    serializer_class = MedecinSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        serializer.save()

class ProfileUpdateView(generics.RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return PatientProfileUpdateSerializer
        elif user.role == 'DOCTOR':
            return MedecinProfileUpdateSerializer
        else:
            raise PermissionDenied("Rôle non autorisé.")

    def get_object(self):
        user = self.request.user
        if user.role == 'PATIENT':
            return user.patient
        elif user.role == 'DOCTOR':
            return user.medecin
        else:
            raise PermissionDenied("Rôle non autorisé.")


class DisponibiliteViewSet(viewsets.ModelViewSet):
    queryset = Disponibilite.objects.all()
    serializer_class = DisponibiliteSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Disponibilite.objects.filter(is_booked=False)
        medecin_id = self.request.query_params.get('medecin')
        if medecin_id:
            queryset = queryset.filter(medecin_id=medecin_id)
        return queryset

    def perform_create(self, serializer):
        user = self.request.user
        if user.role != 'DOCTOR':
            raise PermissionDenied("Seuls les médecins peuvent créer leurs créneaux.")
        medecin = user.medecin
        serializer.save(medecin=medecin)

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

class AgendaView(APIView):
    def get(self, request):
        medecin_id = request.query_params.get('medecin')
        if not medecin_id:
            return Response({"error": "Paramètre 'medecin' requis"}, status=400)

        today = timezone.now()
        dispo_qs = Disponibilite.objects.filter(
            medecin_id=medecin_id,
            date__gte=today
        ).order_by('date')

        slots = []
        for dispo in dispo_qs:
            slots.append({
                "date": dispo.date.isoformat(),
                "is_booked": dispo.is_booked,
                "disponibilite_id": dispo.id
            })

        return Response(slots)
