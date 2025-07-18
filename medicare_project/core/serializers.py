from rest_framework import serializers
from .models import User, Patient, Medecin, RendezVous, Disponibilite
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'first_name', 'last_name', 'role']


class PatientSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Patient
        fields = ['id', 'user', 'phone']


class MedecinSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Medecin
        fields = ['id', 'user', 'specialty']


class RendezVousSerializer(serializers.ModelSerializer):
    medecin = serializers.PrimaryKeyRelatedField(queryset=Medecin.objects.all())
    patient = serializers.PrimaryKeyRelatedField(read_only=True)
    disponibilite = serializers.PrimaryKeyRelatedField(
        queryset=Disponibilite.objects.filter(is_booked=False),
        required=True
    )
    date = serializers.DateTimeField(read_only=True)
    medecin_name = serializers.SerializerMethodField()

    class Meta:
        model = RendezVous
        fields = ['id', 'patient', 'medecin', 'medecin_name', 'date', 'motif', 'disponibilite', 'notes_medicales']

    def get_medecin_name(self, obj):
        return f"{obj.medecin.user.first_name} {obj.medecin.user.last_name}"


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ['id', 'email', 'password', 'role', 'first_name', 'last_name']

    def validate_role(self, value):
        if value not in ["PATIENT", "DOCTOR"]:
            raise serializers.ValidationError("Rôle invalide.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Cet email est déjà utilisé.")
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')

        # ✅ Pop username au cas où
        validated_data.pop('username', None)

        user = User.objects.create_user(**validated_data)
        user.set_password(password)
        user.save()

        if user.role == "PATIENT":
            Patient.objects.create(user=user, phone="")
        elif user.role == "DOCTOR":
            Medecin.objects.create(user=user, specialty="")

        return user


class UserUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

class PatientProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Patient
        fields = ['user', 'phone']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class MedecinProfileUpdateSerializer(serializers.ModelSerializer):
    user = UserUpdateSerializer()

    class Meta:
        model = Medecin
        fields = ['user', 'specialty']

    def update(self, instance, validated_data):
        user_data = validated_data.pop('user')
        for attr, value in user_data.items():
            setattr(instance.user, attr, value)
        instance.user.save()

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()
        return instance

class DisponibiliteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disponibilite
        fields = ['id', 'medecin', 'date', 'is_booked']
        read_only_fields = ["medecin", 'is_booked']


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    """
    Authentifie un utilisateur via email + mot de passe.
    """
    username_field = 'email'
