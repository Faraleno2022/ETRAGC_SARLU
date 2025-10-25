import os
import django
import random
from datetime import date, timedelta

# Configuration Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from apps.planning.models import Tache
from apps.projects.models import Projet
from apps.personnel.models import Personnel

def create_taches():
    """Créer des tâches de test pour les projets"""
    
    print("🚀 Création des tâches de test...")
    
    # Récupérer les projets et le personnel
    projets = Projet.objects.all()
    personnel = Personnel.objects.filter(actif=True)
    
    if not projets.exists():
        print("❌ Aucun projet trouvé. Veuillez d'abord créer des projets.")
        return
    
    # Définir les types de tâches par phase
    taches_par_phase = {
        'Études': [
            'Étude de faisabilité',
            'Étude de sol',
            'Plans architecturaux',
            'Plans de structure',
            'Devis estimatif',
        ],
        'Préparation': [
            'Obtention des permis',
            'Installation du chantier',
            'Clôture du chantier',
            'Mise en place des équipements',
            'Réunion de démarrage',
        ],
        'Gros œuvre': [
            'Terrassement',
            'Fondations',
            'Élévation des murs',
            'Dalle et plancher',
            'Charpente',
            'Couverture',
        ],
        'Second œuvre': [
            'Plomberie',
            'Électricité',
            'Menuiserie',
            'Plâtrerie',
            'Carrelage',
            'Peinture',
        ],
        'Finitions': [
            'Nettoyage final',
            'Aménagements extérieurs',
            'Réception des travaux',
            'Livraison',
        ],
    }
    
    priorites = ['Basse', 'Moyenne', 'Haute', 'Critique']
    statuts = ['A_faire', 'En_cours', 'En_pause', 'Terminée', 'Bloquée']
    
    taches_creees = 0
    
    for projet in projets[:5]:  # Limiter aux 5 premiers projets
        print(f"\n📋 Création des tâches pour le projet: {projet.code_projet}")
        
        ordre = 0
        date_debut_projet = projet.date_debut or date.today()
        
        for phase, taches_noms in taches_par_phase.items():
            # Sélectionner quelques tâches de cette phase
            nb_taches = random.randint(2, len(taches_noms))
            taches_selectionnees = random.sample(taches_noms, nb_taches)
            
            for nom_tache in taches_selectionnees:
                # Calculer les dates
                jours_debut = random.randint(0, 60)
                duree = random.randint(5, 30)
                date_debut = date_debut_projet + timedelta(days=jours_debut)
                date_fin_prevue = date_debut + timedelta(days=duree)
                
                # Déterminer le statut en fonction de la date
                if date_debut > date.today():
                    statut = 'A_faire'
                    progression = 0
                elif date_fin_prevue < date.today():
                    statut = random.choice(['Terminée', 'En_cours', 'Bloquée'])
                    progression = 100 if statut == 'Terminée' else random.randint(60, 95)
                else:
                    statut = random.choice(['En_cours', 'En_pause'])
                    progression = random.randint(10, 80)
                
                # Date de fin réelle si terminée
                date_fin_reelle = None
                if statut == 'Terminée':
                    jours_ecart = random.randint(-5, 10)
                    date_fin_reelle = date_fin_prevue + timedelta(days=jours_ecart)
                
                # Assigner un responsable
                responsable = random.choice(personnel) if personnel.exists() and random.random() > 0.2 else None
                
                # Priorité
                if 'Étude' in nom_tache or 'permis' in nom_tache.lower():
                    priorite = random.choice(['Haute', 'Critique'])
                elif 'Finitions' in phase:
                    priorite = random.choice(['Basse', 'Moyenne'])
                else:
                    priorite = random.choice(priorites)
                
                # Créer la tâche
                try:
                    tache, created = Tache.objects.get_or_create(
                        projet=projet,
                        nom_tache=f"{phase} - {nom_tache}",
                        defaults={
                            'description': f"Tâche de {nom_tache.lower()} pour le projet {projet.nom_projet}",
                            'date_debut': date_debut,
                            'date_fin_prevue': date_fin_prevue,
                            'date_fin_reelle': date_fin_reelle,
                            'priorite': priorite,
                            'statut': statut,
                            'pourcentage_progression': progression,
                            'responsable': responsable,
                            'ordre_affichage': ordre,
                        }
                    )
                    
                    if created:
                        taches_creees += 1
                        print(f"  ✅ Tâche créée: {nom_tache}")
                        print(f"     Statut: {statut} | Priorité: {priorite} | Progression: {progression}%")
                        if responsable:
                            print(f"     Responsable: {responsable.get_full_name()}")
                    
                    ordre += 1
                    
                except Exception as e:
                    print(f"  ❌ Erreur lors de la création de la tâche {nom_tache}: {str(e)}")
    
    print(f"\n✅ {taches_creees} tâches créées avec succès!")
    print(f"📊 Total des tâches dans la base: {Tache.objects.count()}")

if __name__ == '__main__':
    create_taches()
