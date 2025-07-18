from django.core.management.base import BaseCommand
from django.utils import timezone
from django.core.mail import send_mail
from core.models import RendezVous
from django.conf import settings
from datetime import timedelta

class Command(BaseCommand):
    help = "Envoie des rappels automatiques aux patients avant leur rendez-vous"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        limit = now + timedelta(hours=24)

        rdvs = RendezVous.objects.filter(
            date__range=(now, limit),
            rappel_envoye=False
        )

        self.stdout.write(
            f"🔍 Rappels prévus entre {now.strftime('%Y-%m-%d %H:%M')} "
            f"et {limit.strftime('%Y-%m-%d %H:%M')} ➜ {rdvs.count()} RDV trouvés"
        )

        for rdv in rdvs:
            patient_user = rdv.patient.user
            if patient_user.email:
                send_mail(
                    subject="Rappel de votre rendez-vous",
                    message=(
                        f"Bonjour {patient_user.first_name},\n\n"
                        f"Un rappel : vous avez un rendez-vous prévu le {rdv.date}.\n"
                        f"Motif : {rdv.motif}\n\n"
                        "Merci de votre ponctualité.\nL'équipe MediCare."
                    ),
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[patient_user.email],
                    fail_silently=False,
                    html_message=(
                        f"<h2>Bonjour {patient_user.first_name},</h2>"
                        f"<p>Un petit rappel : votre rendez-vous est prévu pour le <strong>{rdv.date}</strong>.</p>"
                        f"<p><strong>Motif :</strong> {rdv.motif}</p>"
                        "<p>Merci de votre ponctualité.<br>L'équipe MediCare.</p>"
                    )
                )
                rdv.rappel_envoye = True
                rdv.save()

                self.stdout.write(
                    self.style.SUCCESS(
                        f"✅ Rappel envoyé à {patient_user.email} pour le RDV {rdv.id}"
                    )
                )
            else:
                self.stdout.write(
                    self.style.WARNING(
                        f"⚠️ Pas d'email pour {patient_user.email} (Patient ID: {rdv.patient.id})"
                    )
                )
