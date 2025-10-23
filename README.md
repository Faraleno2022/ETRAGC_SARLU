# 🏗️ ETRAGC SARLU - Application de Gestion BTP

Application web complète de gestion pour **ÉLITE DES TRAVAUX DE GÉNIE CIVIL SARLU**

## 📋 Fonctionnalités

### 🎯 Modules Principaux
- ✅ **Gestion des Projets** - Suivi complet des chantiers
- 💰 **Gestion Financière** - Dépôts, retraits, dépenses
- 📄 **Devis & Factures** - Génération automatique de documents
- 👷 **Gestion du Personnel** - Affectations et planning
- 📅 **Planning des Travaux** - Diagramme de Gantt interactif
- 📊 **Tableaux de Bord** - Statistiques et rapports en temps réel
- 👥 **Gestion Multi-utilisateurs** - Permissions par rôle

### 🔐 Rôles Utilisateurs
- **Admin** - Accès total
- **Manager** - Gestion projets et finances
- **Comptable** - Finances et facturation
- **Chef de Chantier** - Planning et dépenses quotidiennes
- **Lecteur** - Consultation uniquement

## 🚀 Installation

### Prérequis
- Python 3.10+
- MySQL 8.0+
- pip

### Étapes d'installation

1. **Cloner le projet**
```bash
cd C:\Users\LENO\Desktop\Etragsarlu
```

2. **Créer un environnement virtuel**
```bash
python -m venv venv
venv\Scripts\activate  # Windows
```

3. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

4. **Configurer la base de données**
- Créer la base de données MySQL :
```sql
CREATE DATABASE etragc_db CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

5. **Configurer les variables d'environnement**
```bash
copy .env.example .env
# Éditer .env avec vos paramètres
```

6. **Appliquer les migrations**
```bash
python manage.py makemigrations
python manage.py migrate
```

7. **Créer un superutilisateur**
```bash
python manage.py createsuperuser
```

8. **Charger les données initiales**
```bash
python manage.py loaddata initial_data
```

9. **Lancer le serveur**
```bash
python manage.py runserver
```

10. **Accéder à l'application**
- URL : http://localhost:8000
- Admin : http://localhost:8000/admin

## 📁 Structure du Projet

```
etragc_sarlu/
├── config/                 # Configuration Django
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/              # Fonctionnalités communes
│   ├── accounts/          # Authentification
│   ├── clients/           # Gestion clients
│   ├── projects/          # Gestion projets
│   ├── finances/          # Transactions et dépenses
│   ├── invoicing/         # Devis et factures
│   ├── personnel/         # Gestion personnel
│   ├── planning/          # Planning et tâches
│   └── dashboard/         # Tableaux de bord
├── static/                # Fichiers statiques (CSS, JS, images)
├── media/                 # Fichiers uploadés
├── templates/             # Templates HTML
├── requirements.txt       # Dépendances Python
└── manage.py             # Script de gestion Django
```

## 🎨 Technologies Utilisées

- **Backend** : Django 4.2
- **Base de données** : MySQL 8.0
- **Frontend** : Bootstrap 5, TailwindCSS
- **Charts** : Chart.js
- **Icons** : Font Awesome, Lucide
- **PDF** : ReportLab
- **Excel** : openpyxl, xlsxwriter

## 📊 Modules Détaillés

### 1. Gestion des Projets
- Création et suivi de projets
- Calcul automatique des budgets
- Suivi de l'avancement
- Alertes de dépassement

### 2. Gestion Financière
- Enregistrement des dépôts clients
- Suivi des retraits
- Catégorisation des dépenses
- Rapports financiers automatisés

### 3. Devis et Factures
- Génération de devis pro forma
- Conversion devis → facture
- Numérotation automatique
- Export PDF professionnel
- Suivi des paiements

### 4. Planning des Travaux
- Calendrier interactif
- Diagramme de Gantt
- Affectation du personnel
- Suivi des tâches

### 5. Tableaux de Bord
- Statistiques en temps réel
- Graphiques interactifs
- Indicateurs clés (KPI)
- Exports Excel/PDF

## 🔒 Sécurité

- Authentification Django
- Permissions par rôle
- Hash des mots de passe (PBKDF2)
- Protection CSRF
- Validation des données
- Audit trail complet

## 📱 Responsive Design

L'application est entièrement responsive et fonctionne sur :
- 💻 Desktop
- 📱 Tablettes
- 📱 Smartphones

## 🛠️ Maintenance

### Sauvegarde de la base de données
```bash
python manage.py dumpdata > backup.json
```

### Restauration
```bash
python manage.py loaddata backup.json
```

### Collecte des fichiers statiques
```bash
python manage.py collectstatic
```

## 📞 Support

**ETRAGC SARLU**
- 📧 Email : info@etragc-sarlu.com
- 📱 Téléphone : +224 628 78 78 03 / +224 612 79 79 03
- 🌐 Site web : www.etragc-sarlu.com
- 📍 Adresse : Kankan, Quartier Missira, Guinée

## 📄 Licence

© 2025 ETRAGC SARLU - Tous droits réservés

## 🎯 Version

**Version 1.0** - Octobre 2025

---

Développé avec ❤️ pour ETRAGC SARLU
