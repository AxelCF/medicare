from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView  # ✅ Ajoute bien ça !

from core.views import (
    RegisterView,
    RendezVousViewSet,
    PatientViewSet,
    MedecinViewSet,
    ProfileUpdateView,
    DisponibiliteViewSet,
    CustomTokenObtainPairView,  # ✅ Ton Custom JWT
    AgendaView,
)

router = DefaultRouter()
router.register(r'patients', PatientViewSet)
router.register(r'medecins', MedecinViewSet)
router.register(r'rendezvous', RendezVousViewSet, basename='rendezvous')
router.register(r'disponibilites', DisponibiliteViewSet, basename='disponibilite')

urlpatterns = [
    path('', include(router.urls)),
    path('register/', RegisterView.as_view(), name='register'),
    path('token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),  # ✅ Utilise bien ton custom
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api-auth/', include('rest_framework.urls')),
    path('profile/', ProfileUpdateView.as_view(), name='profile-update'),
    path('agenda/', AgendaView.as_view(), name='agenda'),
]
