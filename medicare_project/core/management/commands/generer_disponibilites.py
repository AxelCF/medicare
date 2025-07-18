from django.core.management.base import BaseCommand
from core.models import PlageHoraire, Disponibilite
from datetime import datetime, timedelta
from django.utils import timezone

class Command(BaseCommand):
    help = "Génère les disponibilités à partir des plages horaires pour les 30 prochains jours"

    def handle(self, *args, **kwargs):
        today = timezone.now().date()
        jours = 30
        total_crees = 0

        for n in range(jours):
            jour = today + timedelta(days=n)
            weekday = jour.weekday()
            plages = PlageHoraire.objects.filter(jour=weekday)

            for plage in plages:
                heure_debut = datetime.combine(jour, plage.heure_debut)
                heure_fin = datetime.combine(jour, plage.heure_fin)

                current = heure_debut
                while current + plage.duree_slot <= heure_fin:
                    # Vérifie si une disponibilité existe déjà
                    if not Disponibilite.objects.filter(medecin=plage.medecin, date=current).exists():
                        Disponibilite.objects.create(
                            medecin=plage.medecin,
                            date=current,
                            is_booked=False
                        )
                        total_crees += 1
                    current += plage.duree_slot

        self.stdout.write(self.style.SUCCESS(f"{total_crees} disponibilités créées."))
