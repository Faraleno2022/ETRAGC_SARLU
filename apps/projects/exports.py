"""
Vues d'export pour le module Projects
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from reportlab.lib.units import cm
from apps.core.utils.exports import ExcelExporter, PDFExporter, format_currency, format_date
from .models import Projet
from datetime import datetime


@login_required
def export_projets_excel(request):
    """Exporter la liste des projets en Excel"""
    # Récupérer les projets avec les mêmes filtres que la liste
    queryset = Projet.objects.select_related('client', 'responsable').all()
    
    # Appliquer les filtres de la requête
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(code_projet__icontains=search) |
            Q(nom_projet__icontains=search) |
            Q(client__nom_complet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut=statut)
    
    # Créer l'exporteur
    filename = f"projets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    exporter = ExcelExporter(filename, "Projets")
    
    # Titre
    exporter.add_title("ETRAGC SARLU - Liste des Projets")
    exporter.add_empty_row()
    
    # Informations
    exporter.add_info("Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M'))
    exporter.add_info("Nombre de projets:", queryset.count())
    exporter.add_empty_row()
    
    # En-têtes
    headers = [
        "Code Projet",
        "Nom du Projet",
        "Client",
        "Statut",
        "Date Début",
        "Date Fin Prévue",
        "Montant Prévu (GNF)",
        "Responsable",
        "Ville"
    ]
    exporter.add_headers(headers)
    
    # Données
    total_montant = 0
    for projet in queryset:
        row = [
            projet.code_projet,
            projet.nom_projet,
            projet.client.nom_complet if projet.client else "N/A",
            projet.get_statut_display(),
            format_date(projet.date_debut),
            format_date(projet.date_fin_prevue),
            float(projet.montant_prevu) if projet.montant_prevu else 0,
            projet.responsable.get_full_name() if projet.responsable else "N/A",
            projet.ville_chantier or "N/A"
        ]
        exporter.add_row(row)
        if projet.montant_prevu:
            total_montant += float(projet.montant_prevu)
    
    # Ligne de total
    exporter.add_row([
        "", "", "", "", "", "TOTAL:",
        total_montant, "", ""
    ], is_total=True)
    
    # Ajuster les colonnes
    exporter.auto_adjust_columns()
    
    return exporter.get_response()


@login_required
def export_projets_pdf(request):
    """Exporter la liste des projets en PDF"""
    from django.db.models import Q
    
    # Récupérer les projets
    queryset = Projet.objects.select_related('client', 'responsable').all()
    
    # Appliquer les filtres
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(code_projet__icontains=search) |
            Q(nom_projet__icontains=search) |
            Q(client__nom_complet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut=statut)
    
    # Créer l'exporteur
    filename = f"projets_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    exporter = PDFExporter(filename, "ETRAGC SARLU - Liste des Projets", orientation='landscape')
    
    # Titre
    exporter.add_title()
    
    # Informations
    info_data = [
        ["Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M')],
        ["Nombre de projets:", str(queryset.count())],
    ]
    exporter.add_info_table(info_data)
    
    # En-têtes et données
    headers = ["Code", "Nom du Projet", "Client", "Statut", "Montant Prévu", "Responsable"]
    
    data = []
    total_montant = 0
    for projet in queryset:
        row = [
            projet.code_projet,
            projet.nom_projet[:30] + "..." if len(projet.nom_projet) > 30 else projet.nom_projet,
            projet.client.nom_complet[:20] if projet.client else "N/A",
            projet.get_statut_display(),
            format_currency(projet.montant_prevu),
            projet.responsable.get_full_name()[:20] if projet.responsable else "N/A"
        ]
        data.append(row)
        if projet.montant_prevu:
            total_montant += float(projet.montant_prevu)
    
    # Ajouter le total
    data.append(["", "", "", "TOTAL:", format_currency(total_montant), ""])
    
    # Largeurs de colonnes
    col_widths = [3*cm, 5*cm, 4*cm, 3*cm, 4*cm, 4*cm]
    exporter.add_data_table(headers, data, col_widths)
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()


@login_required
def export_projet_detail_pdf(request, pk):
    """Exporter les détails d'un projet en PDF"""
    projet = Projet.objects.select_related('client', 'responsable').get(pk=pk)
    
    filename = f"projet_{projet.code_projet}_{datetime.now().strftime('%Y%m%d')}.pdf"
    exporter = PDFExporter(filename, f"Détails du Projet - {projet.code_projet}")
    
    # Titre
    exporter.add_title(f"Projet: {projet.nom_projet}")
    
    # Informations principales
    info_data = [
        ["Code Projet:", projet.code_projet],
        ["Nom:", projet.nom_projet],
        ["Client:", projet.client.nom_complet if projet.client else "N/A"],
        ["Statut:", projet.get_statut_display()],
        ["Date de début:", format_date(projet.date_debut)],
        ["Date de fin prévue:", format_date(projet.date_fin_prevue)],
        ["Montant prévu:", format_currency(projet.montant_prevu)],
        ["Responsable:", projet.responsable.get_full_name() if projet.responsable else "N/A"],
        ["Ville:", projet.ville_chantier or "N/A"],
    ]
    exporter.add_info_table(info_data)
    
    # Description
    if projet.description:
        from reportlab.platypus import Paragraph, Spacer
        from reportlab.lib.units import cm
        exporter.elements.append(Spacer(1, 0.5*cm))
        exporter.elements.append(Paragraph("<b>Description:</b>", exporter.styles['Normal']))
        exporter.elements.append(Paragraph(projet.description, exporter.styles['Normal']))
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()
