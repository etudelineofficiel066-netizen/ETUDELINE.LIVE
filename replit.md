# Étude LINE — Plateforme Éducative FastAPI

## Description
Application web éducative pour professeurs et étudiants (universités sénégalaises).
Technologie : Python / FastAPI + PostgreSQL + Jinja2 templates.

## Architecture
- `main.py` — Application FastAPI principale (routes, logique métier)
- `models.py` — Modèles SQLAlchemy (ORM)
- `database.py` — Configuration de la base de données
- `templates/` — Templates Jinja2 HTML
- `static/` — Fichiers statiques (images, CSS, JS)
- `uploads/` — Fichiers uploadés (cours, exercices, solutions, preuves de paiement)

## Démarrage
```
uvicorn main:app --host 0.0.0.0 --port 5000
```

## Base de données
PostgreSQL via `DATABASE_URL` (env var).
Les tables sont créées automatiquement au démarrage.

## Fonctionnalités principales
- Authentification (admin, professeur, étudiant)
- Gestion académique (universités, UFR, filières, matières)
- Chapitres complets (cours, exercices, solutions)
- Messagerie prof-étudiant
- Cours programmés (Jitsi)
- **Abonnement Premium** — paiement 1000 FCFA/an via Orange Money ou Wave

## Système de paiement (ajouté)
- Paiement 100% manuel au numéro **775771443** (ELN Technologies)
- Étudiant uploade une capture d'écran comme preuve
- Admin valide ou refuse depuis l'onglet "💳 Paiements" du dashboard
- Validation active l'abonnement pour 365 jours
- Solutions bloquées pour les non-abonnés (barrière premium dans chapitre_detail.html)

### Modèles ajoutés/modifiés
- `Etudiant` : +`subscription_active` (Boolean), +`subscription_expires` (DateTime)
- `PaymentRequest` : nouveau modèle (student_id, payment_method, amount, proof_image_path, status, created_at)

### Routes de paiement
- `POST /payments/request` — Étudiant soumet une demande
- `GET /admin/payments` — Liste toutes les demandes (admin)
- `GET /admin/payments/{id}/proof` — Affiche l'image de preuve (admin)
- `POST /admin/payments/{id}/approve` — Valide l'abonnement (admin)
- `POST /admin/payments/{id}/reject` — Refuse la demande (admin)
