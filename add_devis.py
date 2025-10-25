"""
Script pour ajouter des devis de test
"""
import os
import django
from datetime import date, timedelta
from decimal import Decimal

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.invoicing.models import Devis, LigneDevis
from apps.clients.models import Client
from apps.projects.models import Projet
from django.contrib.auth import get_user_model

User = get_user_model()

def create_devis():
    """Créer des devis de test"""
    
    # Récupérer un utilisateur admin
    try:
        admin = User.objects.filter(is_superuser=True).first()
        if not admin:
            print("❌ Aucun utilisateur admin trouvé. Créez d'abord un superutilisateur.")
            return
    except Exception as e:
        print(f"❌ Erreur lors de la récupération de l'utilisateur: {e}")
        return
    
    # Récupérer des clients
    clients = list(Client.objects.all()[:3])
    if not clients:
        print("❌ Aucun client trouvé. Ajoutez d'abord des clients.")
        return
    
    # Récupérer des projets
    projets = list(Projet.objects.all()[:3])
    
    devis_data = [
        {
            'client': clients[0],
            'projet': projets[0] if projets else None,
            'date_emission': date.today() - timedelta(days=30),
            'date_validite': date.today() + timedelta(days=30),
            'statut': 'Accepté',
            'taux_tva': Decimal('18.00'),
            'conditions_paiement': '50% à la commande, 50% à la livraison',
            'notes': 'Devis pour travaux de construction',
            'lignes': [
                {
                    'ordre': 1,
                    'designation': 'Terrassement et fondations',
                    'description': 'Excavation et coulage des fondations',
                    'quantite': Decimal('150.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('25000.00'),
                },
                {
                    'ordre': 2,
                    'designation': 'Élévation des murs',
                    'description': 'Construction des murs en parpaings',
                    'quantite': Decimal('200.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('35000.00'),
                },
                {
                    'ordre': 3,
                    'designation': 'Charpente et toiture',
                    'description': 'Pose de la charpente et couverture',
                    'quantite': Decimal('120.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('45000.00'),
                },
            ]
        },
        {
            'client': clients[1] if len(clients) > 1 else clients[0],
            'projet': projets[1] if len(projets) > 1 else None,
            'date_emission': date.today() - timedelta(days=15),
            'date_validite': date.today() + timedelta(days=45),
            'statut': 'Envoyé',
            'taux_tva': Decimal('18.00'),
            'conditions_paiement': 'Paiement à 30 jours',
            'notes': 'Devis pour rénovation',
            'lignes': [
                {
                    'ordre': 1,
                    'designation': 'Démolition',
                    'description': 'Démolition des anciennes structures',
                    'quantite': Decimal('1.00'),
                    'unite': 'Forfait',
                    'prix_unitaire_ht': Decimal('2500000.00'),
                },
                {
                    'ordre': 2,
                    'designation': 'Rénovation électrique',
                    'description': 'Mise aux normes de l\'installation électrique',
                    'quantite': Decimal('1.00'),
                    'unite': 'Forfait',
                    'prix_unitaire_ht': Decimal('3500000.00'),
                },
                {
                    'ordre': 3,
                    'designation': 'Plomberie',
                    'description': 'Installation complète de plomberie',
                    'quantite': Decimal('1.00'),
                    'unite': 'Forfait',
                    'prix_unitaire_ht': Decimal('2800000.00'),
                },
            ]
        },
        {
            'client': clients[2] if len(clients) > 2 else clients[0],
            'projet': projets[2] if len(projets) > 2 else None,
            'date_emission': date.today() - timedelta(days=5),
            'date_validite': date.today() + timedelta(days=25),
            'statut': 'Brouillon',
            'taux_tva': Decimal('18.00'),
            'conditions_paiement': 'Paiement échelonné sur 3 mois',
            'notes': 'Devis en cours de finalisation',
            'lignes': [
                {
                    'ordre': 1,
                    'designation': 'Étude de sol',
                    'description': 'Analyse géotechnique du terrain',
                    'quantite': Decimal('1.00'),
                    'unite': 'Forfait',
                    'prix_unitaire_ht': Decimal('1500000.00'),
                },
                {
                    'ordre': 2,
                    'designation': 'Plans architecturaux',
                    'description': 'Conception et plans détaillés',
                    'quantite': Decimal('1.00'),
                    'unite': 'Forfait',
                    'prix_unitaire_ht': Decimal('2000000.00'),
                },
            ]
        },
        {
            'client': clients[0],
            'projet': None,
            'date_emission': date.today() - timedelta(days=60),
            'date_validite': date.today() - timedelta(days=10),
            'statut': 'Expiré',
            'taux_tva': Decimal('18.00'),
            'conditions_paiement': 'Paiement comptant',
            'notes': 'Devis expiré - à renouveler',
            'lignes': [
                {
                    'ordre': 1,
                    'designation': 'Peinture intérieure',
                    'description': 'Peinture de toutes les pièces',
                    'quantite': Decimal('250.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('8000.00'),
                },
                {
                    'ordre': 2,
                    'designation': 'Carrelage',
                    'description': 'Pose de carrelage dans les pièces d\'eau',
                    'quantite': Decimal('80.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('15000.00'),
                },
            ]
        },
        {
            'client': clients[1] if len(clients) > 1 else clients[0],
            'projet': None,
            'date_emission': date.today() - timedelta(days=45),
            'date_validite': date.today() - timedelta(days=5),
            'statut': 'Refusé',
            'taux_tva': Decimal('18.00'),
            'conditions_paiement': 'Paiement à 60 jours',
            'notes': 'Devis refusé par le client - tarif trop élevé',
            'lignes': [
                {
                    'ordre': 1,
                    'designation': 'Extension de bâtiment',
                    'description': 'Construction d\'une extension de 50m²',
                    'quantite': Decimal('50.00'),
                    'unite': 'm²',
                    'prix_unitaire_ht': Decimal('80000.00'),
                },
            ]
        },
    ]
    
    print("\n🚀 Création des devis de test...\n")
    
    created_count = 0
    for data in devis_data:
        try:
            # Créer le devis
            lignes_data = data.pop('lignes')
            devis = Devis.objects.create(
                cree_par=admin,
                **data
            )
            
            # Créer les lignes
            for ligne_data in lignes_data:
                LigneDevis.objects.create(
                    devis=devis,
                    **ligne_data
                )
            
            # Recalculer le montant total
            devis.calculer_montant_total()
            
            created_count += 1
            print(f"✅ Devis créé: {devis.numero_devis} - {devis.client.nom_complet}")
            print(f"   Statut: {devis.statut}")
            print(f"   Montant HT: {devis.montant_ht:,.0f} GNF")
            print(f"   Montant TTC: {devis.montant_ttc:,.0f} GNF")
            print()
            
        except Exception as e:
            print(f"❌ Erreur lors de la création d'un devis: {e}")
            continue
    
    print(f"\n✅ {created_count} devis créés avec succès!")
    print(f"📊 Total des devis dans la base: {Devis.objects.count()}")

if __name__ == '__main__':
    create_devis()
