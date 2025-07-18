# 🏥 MediCare Project — Plateforme de Gestion de Rendez-vous Médicaux

API REST construite avec **Django**, **Django REST Framework** et **JWT** pour gérer les rendez-vous médicaux, les patients, les médecins et la sécurité par rôle.

---

## 🚀 **Fonctionnalités**

- Authentification sécurisée via **JWT**
- Rôles supportés : `PATIENT`, `DOCTOR`, `ADMIN`
- Les Patients peuvent :
  - Réserver un rendez-vous
  - Voir uniquement leurs propres rendez-vous
- Les Médecins :
  - Peuvent consulter leurs rendez-vous
  - Ne peuvent pas créer de rendez-vous eux-mêmes
- Les Admins :
  - Peuvent créer des rendez-vous pour n’importe quel Patient
  - Peuvent lister tous les rendez-vous
- Sécurité :
  - Permissions filtrées par rôle dans les ViewSets
  - Injection automatique du champ `patient` côté backend pour les Patients

---

## ⚙️ **Technologies**

- Python 3.x
- Django
- Django REST Framework
- Django REST Framework Simple JWT
- SQLite (ou PostgreSQL)
- Tests automatisés avec `APITestCase` (DRF)

---

## 📂 **Structure principale**

```bash
/medicare_project
├── /core
│   ├── models.py
│   ├── serializers.py
│   ├── views.py
│   ├── tests.py
├── /config
│   ├── urls.py
├── manage.py
├── requirements.txt
```
