"""
Vues d'export pour le module Invoicing (Devis et Factures)
"""
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Q
from reportlab.lib.units import cm
from apps.core.utils.exports import ExcelExporter, PDFExporter, format_currency, format_date
from .models import Devis, Facture
from datetime import datetime


# ===== EXPORTS DEVIS =====

@login_required
def export_devis_excel(request):
    """Exporter la liste des devis en Excel"""
    queryset = Devis.objects.select_related('client', 'projet').all()
    
    # Appliquer les filtres
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(numero_devis__icontains=search) |
            Q(client__nom_complet__icontains=search) |
            Q(projet__nom_projet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut=statut)
    
    # Créer l'exporteur
    filename = f"devis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    exporter = ExcelExporter(filename, "Devis")
    
    # Titre
    exporter.add_title("ETRAGC SARLU - Liste des Devis")
    exporter.add_empty_row()
    
    # Informations
    exporter.add_info("Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M'))
    exporter.add_info("Nombre de devis:", queryset.count())
    exporter.add_empty_row()
    
    # En-têtes
    headers = [
        "N° Devis",
        "Date",
        "Client",
        "Projet",
        "Montant HT (GNF)",
        "TVA (%)",
        "Montant TTC (GNF)",
        "Statut",
        "Validité (jours)"
    ]
    exporter.add_headers(headers)
    
    # Données
    total_ht = 0
    total_ttc = 0
    for devis in queryset:
        row = [
            devis.numero_devis,
            format_date(devis.date_emission),
            devis.client.nom_complet if devis.client else "N/A",
            devis.projet.nom_projet if devis.projet else "N/A",
            float(devis.montant_ht) if devis.montant_ht else 0,
            float(devis.taux_tva) if devis.taux_tva else 0,
            float(devis.montant_ttc) if devis.montant_ttc else 0,
            devis.get_statut_display(),
            devis.validite_jours or "N/A"
        ]
        exporter.add_row(row)
        if devis.montant_ht:
            total_ht += float(devis.montant_ht)
        if devis.montant_ttc:
            total_ttc += float(devis.montant_ttc)
    
    # Ligne de total
    exporter.add_row([
        "", "", "", "TOTAL:",
        total_ht, "", total_ttc, "", ""
    ], is_total=True)
    
    # Ajuster les colonnes
    exporter.auto_adjust_columns()
    
    return exporter.get_response()


@login_required
def export_devis_pdf(request):
    """Exporter la liste des devis en PDF"""
    queryset = Devis.objects.select_related('client', 'projet').all()
    
    # Appliquer les filtres
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(numero_devis__icontains=search) |
            Q(client__nom_complet__icontains=search) |
            Q(projet__nom_projet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut=statut)
    
    # Créer l'exporteur
    filename = f"devis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    exporter = PDFExporter(filename, "ETRAGC SARLU - Liste des Devis", orientation='landscape')
    
    # Titre
    exporter.add_title()
    
    # Informations
    info_data = [
        ["Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M')],
        ["Nombre de devis:", str(queryset.count())],
    ]
    exporter.add_info_table(info_data)
    
    # En-têtes et données
    headers = ["N° Devis", "Date", "Client", "Projet", "Montant HT", "Montant TTC", "Statut"]
    
    data = []
    total_ht = 0
    total_ttc = 0
    for devis in queryset:
        row = [
            devis.numero_devis,
            format_date(devis.date_emission),
            devis.client.nom_complet[:20] if devis.client else "N/A",
            devis.projet.nom_projet[:25] if devis.projet else "N/A",
            format_currency(devis.montant_ht),
            format_currency(devis.montant_ttc),
            devis.get_statut_display()
        ]
        data.append(row)
        if devis.montant_ht:
            total_ht += float(devis.montant_ht)
        if devis.montant_ttc:
            total_ttc += float(devis.montant_ttc)
    
    # Ajouter le total
    data.append(["", "", "", "TOTAL:", format_currency(total_ht), format_currency(total_ttc), ""])
    
    # Largeurs de colonnes
    col_widths = [3*cm, 2.5*cm, 4*cm, 5*cm, 3.5*cm, 3.5*cm, 2.5*cm]
    exporter.add_data_table(headers, data, col_widths)
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()


@login_required
def export_devis_detail_pdf(request, pk):
    """Exporter les détails d'un devis en PDF"""
    devis = Devis.objects.select_related('client', 'projet').prefetch_related('lignes').get(pk=pk)
    
    filename = f"devis_{devis.numero_devis}_{datetime.now().strftime('%Y%m%d')}.pdf"
    exporter = PDFExporter(filename, f"Devis N° {devis.numero_devis}")
    
    # Titre
    exporter.add_title(f"DEVIS N° {devis.numero_devis}")
    
    # Informations principales
    info_data = [
        ["Date d'émission:", format_date(devis.date_emission)],
        ["Date de validité:", format_date(devis.date_validite)],
        ["Client:", devis.client.nom_complet if devis.client else "N/A"],
        ["Projet:", devis.projet.nom_projet if devis.projet else "N/A"],
        ["Statut:", devis.get_statut_display()],
    ]
    exporter.add_info_table(info_data)
    
    # Lignes du devis
    if devis.lignes.exists():
        from reportlab.platypus import Spacer
        exporter.elements.append(Spacer(1, 0.5*cm))
        
        headers = ["Description", "Quantité", "Prix Unit. (GNF)", "Montant (GNF)"]
        data = []
        
        for ligne in devis.lignes.all():
            data.append([
                ligne.description[:40] if ligne.description else ligne.designation[:40],
                str(ligne.quantite),
                format_currency(ligne.prix_unitaire_ht),
                format_currency(ligne.montant_ht)
            ])
        
        col_widths = [8*cm, 2*cm, 4*cm, 4*cm]
        exporter.add_data_table(headers, data, col_widths)
    
    # Totaux
    from reportlab.platypus import Spacer
    exporter.elements.append(Spacer(1, 0.5*cm))
    
    totaux_data = [
        ["Montant HT:", format_currency(devis.montant_ht)],
        ["TVA (" + str(devis.taux_tva) + "%):", format_currency(devis.montant_tva)],
        ["Montant TTC:", format_currency(devis.montant_ttc)],
    ]
    exporter.add_info_table(totaux_data)
    
    # Notes
    if devis.notes:
        from reportlab.platypus import Paragraph, Spacer
        exporter.elements.append(Spacer(1, 0.5*cm))
        exporter.elements.append(Paragraph("<b>Notes:</b>", exporter.styles['Normal']))
        exporter.elements.append(Paragraph(devis.notes, exporter.styles['Normal']))
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()


# ===== EXPORTS FACTURES =====

@login_required
def export_factures_excel(request):
    """Exporter la liste des factures en Excel"""
    queryset = Facture.objects.select_related('client', 'projet', 'devis').all()
    
    # Appliquer les filtres
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(numero_facture__icontains=search) |
            Q(client__nom_complet__icontains=search) |
            Q(projet__nom_projet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut_paiement=statut)
    
    # Créer l'exporteur
    filename = f"factures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"
    exporter = ExcelExporter(filename, "Factures")
    
    # Titre
    exporter.add_title("ETRAGC SARLU - Liste des Factures")
    exporter.add_empty_row()
    
    # Informations
    exporter.add_info("Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M'))
    exporter.add_info("Nombre de factures:", queryset.count())
    exporter.add_empty_row()
    
    # En-têtes
    headers = [
        "N° Facture",
        "Date",
        "Client",
        "Projet",
        "Montant HT (GNF)",
        "TVA (%)",
        "Montant TTC (GNF)",
        "Montant Payé (GNF)",
        "Reste à Payer (GNF)",
        "Statut",
        "Échéance"
    ]
    exporter.add_headers(headers)
    
    # Données
    total_ht = 0
    total_ttc = 0
    total_paye = 0
    total_reste = 0
    
    for facture in queryset:
        reste = float(facture.montant_ttc or 0) - float(facture.montant_paye or 0)
        row = [
            facture.numero_facture,
            format_date(facture.date_emission),
            facture.client.nom_complet if facture.client else "N/A",
            facture.projet.nom_projet if facture.projet else "N/A",
            float(facture.montant_ht) if facture.montant_ht else 0,
            float(facture.taux_tva) if facture.taux_tva else 0,
            float(facture.montant_ttc) if facture.montant_ttc else 0,
            float(facture.montant_paye) if facture.montant_paye else 0,
            reste,
            facture.get_statut_paiement_display(),
            format_date(facture.date_echeance)
        ]
        exporter.add_row(row)
        
        if facture.montant_ht:
            total_ht += float(facture.montant_ht)
        if facture.montant_ttc:
            total_ttc += float(facture.montant_ttc)
        if facture.montant_paye:
            total_paye += float(facture.montant_paye)
        total_reste += reste
    
    # Ligne de total
    exporter.add_row([
        "", "", "", "TOTAL:",
        total_ht, "", total_ttc, total_paye, total_reste, "", ""
    ], is_total=True)
    
    # Ajuster les colonnes
    exporter.auto_adjust_columns()
    
    return exporter.get_response()


@login_required
def export_factures_pdf(request):
    """Exporter la liste des factures en PDF"""
    queryset = Facture.objects.select_related('client', 'projet').all()
    
    # Appliquer les filtres
    search = request.GET.get('search')
    if search:
        queryset = queryset.filter(
            Q(numero_facture__icontains=search) |
            Q(client__nom_complet__icontains=search) |
            Q(projet__nom_projet__icontains=search)
        )
    
    statut = request.GET.get('statut')
    if statut:
        queryset = queryset.filter(statut_paiement=statut)
    
    # Créer l'exporteur
    filename = f"factures_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
    exporter = PDFExporter(filename, "ETRAGC SARLU - Liste des Factures", orientation='landscape')
    
    # Titre
    exporter.add_title()
    
    # Informations
    info_data = [
        ["Date d'export:", datetime.now().strftime('%d/%m/%Y %H:%M')],
        ["Nombre de factures:", str(queryset.count())],
    ]
    exporter.add_info_table(info_data)
    
    # En-têtes et données
    headers = ["N° Facture", "Date", "Client", "Montant TTC", "Payé", "Reste", "Statut"]
    
    data = []
    total_ttc = 0
    total_paye = 0
    total_reste = 0
    
    for facture in queryset:
        reste = float(facture.montant_ttc or 0) - float(facture.montant_paye or 0)
        row = [
            facture.numero_facture,
            format_date(facture.date_emission),
            facture.client.nom_complet[:25] if facture.client else "N/A",
            format_currency(facture.montant_ttc),
            format_currency(facture.montant_paye),
            format_currency(reste),
            facture.get_statut_paiement_display()
        ]
        data.append(row)
        
        if facture.montant_ttc:
            total_ttc += float(facture.montant_ttc)
        if facture.montant_paye:
            total_paye += float(facture.montant_paye)
        total_reste += reste
    
    # Ajouter le total
    data.append(["", "", "TOTAL:", format_currency(total_ttc), format_currency(total_paye), format_currency(total_reste), ""])
    
    # Largeurs de colonnes
    col_widths = [3*cm, 2.5*cm, 5*cm, 3.5*cm, 3.5*cm, 3.5*cm, 2.5*cm]
    exporter.add_data_table(headers, data, col_widths)
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()


@login_required
def export_facture_detail_pdf(request, pk):
    """Exporter les détails d'une facture en PDF"""
    facture = Facture.objects.select_related('client', 'projet', 'devis').prefetch_related('lignes').get(pk=pk)
    
    filename = f"facture_{facture.numero_facture}_{datetime.now().strftime('%Y%m%d')}.pdf"
    exporter = PDFExporter(filename, f"Facture N° {facture.numero_facture}")
    
    # Titre
    exporter.add_title(f"FACTURE N° {facture.numero_facture}")
    
    # Informations principales
    info_data = [
        ["Date d'émission:", format_date(facture.date_emission)],
        ["Date d'échéance:", format_date(facture.date_echeance)],
        ["Client:", facture.client.nom_complet if facture.client else "N/A"],
        ["Projet:", facture.projet.nom_projet if facture.projet else "N/A"],
        ["Statut:", facture.get_statut_paiement_display()],
    ]
    if facture.devis:
        info_data.append(["Devis associé:", facture.devis.numero_devis])
    
    exporter.add_info_table(info_data)
    
    # Lignes de la facture
    if facture.lignes.exists():
        from reportlab.platypus import Spacer
        exporter.elements.append(Spacer(1, 0.5*cm))
        
        headers = ["Description", "Quantité", "Prix Unit. (GNF)", "Montant (GNF)"]
        data = []
        
        for ligne in facture.lignes.all():
            data.append([
                ligne.description[:40] if ligne.description else ligne.designation[:40],
                str(ligne.quantite),
                format_currency(ligne.prix_unitaire_ht),
                format_currency(ligne.montant_ht)
            ])
        
        col_widths = [8*cm, 2*cm, 4*cm, 4*cm]
        exporter.add_data_table(headers, data, col_widths)
    
    # Totaux
    from reportlab.platypus import Spacer
    exporter.elements.append(Spacer(1, 0.5*cm))
    
    reste = float(facture.montant_ttc or 0) - float(facture.montant_paye or 0)
    totaux_data = [
        ["Montant HT:", format_currency(facture.montant_ht)],
        ["TVA (" + str(facture.taux_tva) + "%):", format_currency(facture.montant_tva)],
        ["Montant TTC:", format_currency(facture.montant_ttc)],
        ["Montant payé:", format_currency(facture.montant_paye)],
        ["Reste à payer:", format_currency(reste)],
    ]
    exporter.add_info_table(totaux_data)
    
    # Notes
    if facture.notes:
        from reportlab.platypus import Paragraph, Spacer
        exporter.elements.append(Spacer(1, 0.5*cm))
        exporter.elements.append(Paragraph("<b>Notes:</b>", exporter.styles['Normal']))
        exporter.elements.append(Paragraph(facture.notes, exporter.styles['Normal']))
    
    # Footer
    exporter.add_footer_info(f"Document généré le {datetime.now().strftime('%d/%m/%Y à %H:%M')} - ETRAGC SARLU")
    
    return exporter.get_response()
