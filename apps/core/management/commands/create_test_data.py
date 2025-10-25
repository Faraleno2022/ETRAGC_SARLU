from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import datetime, timedelta
from decimal import Decimal
import random

from apps.clients.models import Client
from apps.projects.models import Projet
from apps.personnel.models import Personnel, AffectationPersonnel, PaiementPersonnel
from apps.finances.models import Transaction, Depense, CategorieDepense, Fournisseur
from apps.invoicing.models import Facture, LigneFacture

User = get_user_model()


class Command(BaseCommand):
    help = 'Crée des données de test pour le système'

    def handle(self, *args, **kwargs):
        self.stdout.write(self.style.SUCCESS('Création des données de test...'))
        
        # Créer un utilisateur admin si nécessaire
        user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@etragc.com',
                'first_name': 'Admin',
                'last_name': 'ETRAGC',
                'is_staff': True,
                'is_superuser': True
            }
        )
        if created:
            user.set_password('admin123')
            user.save()
            self.stdout.write(self.style.SUCCESS(f'✓ Utilisateur admin créé'))
        
        # Créer des clients
        clients_data = [
            {'nom_complet': 'Mamadou Diallo', 'telephone': '622123456', 'email': 'mdiallo@gmail.com', 'ville': 'Conakry'},
            {'nom_complet': 'Fatoumata Bah', 'telephone': '655987654', 'email': 'fbah@yahoo.fr', 'ville': 'Conakry'},
            {'nom_complet': 'Alpha Condé', 'telephone': '628456789', 'email': 'aconde@hotmail.com', 'ville': 'Kindia'},
        ]
        
        clients = []
        for data in clients_data:
            client, created = Client.objects.get_or_create(
                nom_complet=data['nom_complet'],
                defaults=data
            )
            clients.append(client)
            if created:
                self.stdout.write(f'✓ Client créé: {client.nom_complet}')
        
        # Créer des catégories de dépenses
        categories_data = [
            {'nom': 'Matériaux de construction', 'code': 'MAT', 'couleur_hex': '#3B82F6'},
            {'nom': 'Main d\'œuvre', 'code': 'MO', 'couleur_hex': '#EF4444'},
            {'nom': 'Transport', 'code': 'TRA', 'couleur_hex': '#10B981'},
            {'nom': 'Équipement', 'code': 'EQP', 'couleur_hex': '#F59E0B'},
            {'nom': 'Autres', 'code': 'AUT', 'couleur_hex': '#6B7280'},
        ]
        
        categories = []
        for i, data in enumerate(categories_data):
            cat, created = CategorieDepense.objects.get_or_create(
                code=data['code'],
                defaults={**data, 'ordre_affichage': i}
            )
            categories.append(cat)
            if created:
                self.stdout.write(f'✓ Catégorie créée: {cat.nom}')
        
        # Créer des fournisseurs
        fournisseurs_data = [
            {'nom': 'Quincaillerie Moderne', 'type': 'Matériaux', 'telephone': '622111222'},
            {'nom': 'Transport Express', 'type': 'Transport', 'telephone': '655333444'},
            {'nom': 'Équipements Pro', 'type': 'Equipement', 'telephone': '628555666'},
        ]
        
        fournisseurs = []
        for data in fournisseurs_data:
            fournisseur, created = Fournisseur.objects.get_or_create(
                nom=data['nom'],
                defaults=data
            )
            fournisseurs.append(fournisseur)
            if created:
                self.stdout.write(f'✓ Fournisseur créé: {fournisseur.nom}')
        
        # Créer du personnel
        personnel_data = [
            {'nom': 'Camara', 'prenom': 'Ibrahima', 'fonction': 'Chef_Chantier', 'type_contrat': 'CDI', 'salaire_journalier': 150000},
            {'nom': 'Sylla', 'prenom': 'Mohamed', 'fonction': 'Maçon', 'type_contrat': 'Journalier', 'salaire_journalier': 80000},
            {'nom': 'Kouyaté', 'prenom': 'Sékou', 'fonction': 'Ferrailleur', 'type_contrat': 'Journalier', 'salaire_journalier': 75000},
            {'nom': 'Touré', 'prenom': 'Amadou', 'fonction': 'Électricien', 'type_contrat': 'CDD', 'salaire_journalier': 100000},
            {'nom': 'Barry', 'prenom': 'Thierno', 'fonction': 'Plombier', 'type_contrat': 'CDD', 'salaire_journalier': 95000},
        ]
        
        personnels = []
        for data in personnel_data:
            pers, created = Personnel.objects.get_or_create(
                nom=data['nom'],
                prenom=data['prenom'],
                defaults={
                    **data,
                    'telephone': f"62{random.randint(1000000, 9999999)}",
                    'date_embauche': datetime.now().date() - timedelta(days=random.randint(30, 365))
                }
            )
            personnels.append(pers)
            if created:
                self.stdout.write(f'✓ Personnel créé: {pers.get_full_name()}')
        
        # Créer des projets
        projets_data = [
            {
                'nom_projet': 'Construction Villa Moderne - Kaloum',
                'client': clients[0],
                'montant_prevu': 150000000,
                'date_debut': datetime.now().date() - timedelta(days=60),
                'date_fin_prevue': datetime.now().date() + timedelta(days=120),
                'statut': 'En_cours',
                'pourcentage_avancement': 35,
                'ville_chantier': 'Conakry',
            },
            {
                'nom_projet': 'Rénovation Immeuble Commercial - Matam',
                'client': clients[1],
                'montant_prevu': 85000000,
                'date_debut': datetime.now().date() - timedelta(days=30),
                'date_fin_prevue': datetime.now().date() + timedelta(days=90),
                'statut': 'En_cours',
                'pourcentage_avancement': 20,
                'ville_chantier': 'Conakry',
            },
            {
                'nom_projet': 'Construction Entrepôt - Kindia',
                'client': clients[2],
                'montant_prevu': 200000000,
                'date_debut': datetime.now().date() - timedelta(days=90),
                'date_fin_prevue': datetime.now().date() + timedelta(days=60),
                'statut': 'En_cours',
                'pourcentage_avancement': 65,
                'ville_chantier': 'Kindia',
            },
        ]
        
        projets = []
        for data in projets_data:
            projet, created = Projet.objects.get_or_create(
                nom_projet=data['nom_projet'],
                defaults={**data, 'responsable': user}
            )
            projets.append(projet)
            if created:
                self.stdout.write(f'✓ Projet créé: {projet.code_projet}')
        
        # Créer des transactions pour chaque projet
        for projet in projets:
            # Dépôts
            for i in range(3):
                Transaction.objects.get_or_create(
                    projet=projet,
                    type='Dépôt',
                    date_transaction=projet.date_debut + timedelta(days=i*15),
                    defaults={
                        'montant': Decimal(projet.montant_prevu) * Decimal('0.3'),
                        'mode_paiement': random.choice(['Virement', 'Chèque']),
                        'saisi_par': user,
                        'reference': f'DEP-{projet.code_projet}-{i+1}'
                    }
                )
            
            # Retraits
            for i in range(2):
                Transaction.objects.get_or_create(
                    projet=projet,
                    type='Retrait',
                    date_transaction=projet.date_debut + timedelta(days=10+i*20),
                    defaults={
                        'montant': Decimal(projet.montant_prevu) * Decimal('0.15'),
                        'mode_paiement': 'Espèces',
                        'saisi_par': user,
                        'reference': f'RET-{projet.code_projet}-{i+1}'
                    }
                )
        
        self.stdout.write(f'✓ Transactions créées pour {len(projets)} projets')
        
        # Créer des dépenses pour chaque projet
        for projet in projets:
            nb_depenses = random.randint(10, 20)
            for i in range(nb_depenses):
                date_depense = projet.date_debut + timedelta(days=random.randint(0, 60))
                Depense.objects.get_or_create(
                    projet=projet,
                    date_depense=date_depense,
                    categorie=random.choice(categories),
                    defaults={
                        'fournisseur': random.choice(fournisseurs) if random.random() > 0.3 else None,
                        'montant': Decimal(random.randint(50000, 5000000)),
                        'mode_paiement': random.choice(['Espèces', 'Chèque', 'Virement', 'Mobile_Money']),
                        'statut': 'Validée',
                        'saisi_par': user,
                        'description': f'Dépense {i+1} pour {projet.nom_projet}'
                    }
                )
        
        self.stdout.write(f'✓ Dépenses créées pour {len(projets)} projets')
        
        # Créer des factures pour chaque projet
        for projet in projets:
            for i in range(random.randint(1, 3)):
                montant_ht = Decimal(projet.montant_prevu) * Decimal('0.3')
                montant_ttc = montant_ht * Decimal('1.18')  # Avec TVA 18%
                montant_paye = montant_ttc if random.random() > 0.5 else (montant_ttc * Decimal('0.5') if random.random() > 0.5 else Decimal('0'))
                
                # Déterminer le statut en fonction du montant payé
                if montant_paye >= montant_ttc:
                    statut = 'Payée'
                elif montant_paye > 0:
                    statut = 'Partielle'
                else:
                    statut = 'Impayée'
                
                facture, created = Facture.objects.get_or_create(
                    numero_facture=f'FACT-{projet.code_projet}-{i+1:03d}',
                    defaults={
                        'projet': projet,
                        'client': projet.client,
                        'date_emission': projet.date_debut + timedelta(days=i*30),
                        'date_echeance': projet.date_debut + timedelta(days=i*30+30),
                        'montant_ht': montant_ht,
                        'taux_tva': Decimal('18.00'),
                        'montant_paye': montant_paye,
                        'statut_paiement': statut,
                        'notes': f'Facture {i+1} pour {projet.nom_projet}',
                        'cree_par': user
                    }
                )
        
        self.stdout.write(f'✓ Factures créées pour {len(projets)} projets')
        
        # Affecter du personnel aux projets et créer des paiements
        for projet in projets:
            # Affecter 3-4 personnes par projet
            nb_personnel = random.randint(3, 4)
            personnel_affecte = random.sample(personnels, nb_personnel)
            
            for pers in personnel_affecte:
                affectation, created = AffectationPersonnel.objects.get_or_create(
                    personnel=pers,
                    projet=projet,
                    date_debut=projet.date_debut,
                    defaults={
                        'role_chantier': random.choice(['Chef', 'Superviseur', 'Ouvrier', 'Technicien']),
                        'notes': f'Affecté au projet {projet.nom_projet}'
                    }
                )
                
                # Créer des paiements pour ce personnel sur ce projet
                nb_paiements = random.randint(2, 5)
                for i in range(nb_paiements):
                    date_paiement = projet.date_debut + timedelta(days=i*15)
                    if date_paiement <= datetime.now().date():
                        nombre_jours = random.randint(5, 20) if pers.type_contrat == 'Journalier' else None
                        montant = pers.salaire_journalier * nombre_jours if nombre_jours else pers.salaire_journalier * 15
                        
                        PaiementPersonnel.objects.get_or_create(
                            personnel=pers,
                            projet=projet,
                            date_paiement=date_paiement,
                            defaults={
                                'montant': Decimal(montant),
                                'nombre_jours': nombre_jours,
                                'mode_paiement': random.choice(['Espèces', 'Virement', 'Mobile_Money']),
                                'statut': 'Validé',
                                'saisi_par': user,
                                'valide_par': user,
                                'date_validation': timezone.now(),
                                'description': f'Paiement période {i+1}'
                            }
                        )
        
        self.stdout.write(f'✓ Personnel affecté et paiements créés pour {len(projets)} projets')
        
        self.stdout.write(self.style.SUCCESS('\n✅ Données de test créées avec succès!'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(clients)} clients'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(projets)} projets'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(personnels)} membres du personnel'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(categories)} catégories de dépenses'))
        self.stdout.write(self.style.SUCCESS(f'   - {len(fournisseurs)} fournisseurs'))
        self.stdout.write(self.style.SUCCESS('\nVous pouvez maintenant vous connecter avec:'))
        self.stdout.write(self.style.WARNING('   Username: admin'))
        self.stdout.write(self.style.WARNING('   Password: admin123'))
