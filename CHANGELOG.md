# Changelog - ETRAGC SARLU

## [Version 1.1] - 19 Octobre 2025

### ✨ Nouvelles Fonctionnalités

#### Navigation Améliorée
- ✅ **Barre de navigation horizontale** en haut de page (au lieu de la sidebar)
- ✅ Navigation fixe qui reste visible lors du défilement
- ✅ Menu responsive avec bouton hamburger pour mobile
- ✅ Tous les modules accessibles depuis la barre de navigation

#### Page d'Accueil
- ✅ **Nouvelle page d'accueil** présentant l'entreprise
- ✅ Section Hero avec nom complet de l'entreprise
- ✅ Cartes d'information (Certification, Localisation, Contact)
- ✅ Présentation des domaines d'expertise:
  - Génie Civil
  - Travaux Routiers
  - Hydraulique
  - Ouvrages d'Art
- ✅ Section "Nos Valeurs" (Excellence, Intégrité, Innovation, Collaboration)
- ✅ Statistiques en temps réel:
  - Nombre de projets
  - Nombre de clients
  - Personnel qualifié
  - Années d'expérience

### 🎨 Améliorations de l'Interface

#### Design
- Navigation moderne avec dégradé bleu
- Icônes Font Awesome pour tous les éléments
- Cartes colorées avec bordures distinctives
- Layout responsive et professionnel

#### Expérience Utilisateur
- Menu "Accueil" ajouté comme premier élément
- Accès rapide au tableau de bord et aux projets depuis l'accueil
- Informations de contact facilement accessibles
- Design cohérent sur toutes les pages

### 🔧 Modifications Techniques

#### Structure
- Création du module `apps.core` pour la page d'accueil
- Nouveau fichier `apps/core/views.py`
- Nouveau fichier `apps/core/urls.py`
- Template `templates/core/home.html`

#### Configuration
- Mise à jour de `config/urls.py` pour inclure le module core
- Redirection de la racine (/) vers la page d'accueil
- Template de base `base.html` restructuré

#### Styling
- Suppression du layout avec sidebar
- Ajout de styles pour la navigation horizontale
- Padding-top ajouté au body pour compenser la navbar fixe
- Classes CSS pour la navigation active

### 📱 Responsive Design
- Navigation collapse sur mobile
- Bouton hamburger pour le menu mobile
- Cartes empilées verticalement sur petits écrans
- Grid responsive pour les services et statistiques

---

## [Version 1.0] - 19 Octobre 2025

### 🎉 Version Initiale

#### Modules Implémentés
- ✅ Accounts (Authentification et gestion utilisateurs)
- ✅ Dashboard (Tableau de bord avec statistiques)
- ✅ Clients (Gestion des clients)
- ✅ Projects (Gestion des projets)
- ✅ Finances (Transactions et dépenses)
- 🔄 Invoicing (Structure de base)
- 🔄 Personnel (Structure de base)
- 🔄 Planning (Structure de base)

#### Fonctionnalités
- Authentification complète
- Gestion des projets avec suivi budgétaire
- Gestion des clients
- Système de transactions financières
- Gestion des dépenses avec validation
- Tableaux de bord avec statistiques
- 5 rôles utilisateurs (Admin, Manager, Comptable, Chef de Chantier, Lecteur)

#### Technologies
- Django 4.2.7
- Bootstrap 5
- Font Awesome 6
- SQLite3 (développement)
- Chart.js

---

## 🚀 Prochaines Versions Prévues

### Version 1.2 (À venir)
- [ ] Compléter le module Facturation
- [ ] Génération de PDF pour devis et factures
- [ ] Export Excel des données

### Version 1.3 (À venir)
- [ ] Module Personnel complet
- [ ] Gestion des affectations
- [ ] Suivi des présences

### Version 2.0 (À venir)
- [ ] Module Planning avec calendrier
- [ ] Diagramme de Gantt
- [ ] Notifications par email
- [ ] Rapports avancés

---

**Développé pour ETRAGC SARLU**
