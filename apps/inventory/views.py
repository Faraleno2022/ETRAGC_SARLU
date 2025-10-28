from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Q, F, Count
from django.http import JsonResponse
from django.utils import timezone
from django.core.paginator import Paginator
from decimal import Decimal

from .models import (
    UniteMessure, CategorieProduit, Produit, Stock,
    Achat, LigneAchat, MouvementStock
)
from .forms import (
    UniteMessureForm, CategorieProduitForm, ProduitForm, StockForm,
    AchatForm, LigneAchatFormSet, MouvementStockForm,
    StockFilterForm, AchatFilterForm
)
from apps.projects.models import Projet


# ============ DASHBOARD ============

@login_required
def inventory_dashboard(request):
    """Dashboard de gestion de stock"""
    # Statistiques générales
    total_produits = Produit.objects.filter(actif=True).count()
    total_stocks = Stock.objects.count()
    
    # Valeur totale du stock
    valeur_totale = Stock.objects.aggregate(total=Sum('valeur_stock'))['total'] or 0
    
    # Produits avec stock faible
    stocks_faibles = Stock.objects.select_related('produit', 'projet').filter(
        quantite_actuelle__lt=F('produit__stock_minimum')
    ).order_by('quantite_actuelle')[:10]
    
    # Achats récents
    achats_recents = Achat.objects.select_related('projet', 'fournisseur').order_by('-date_achat')[:10]
    
    # Mouvements récents
    mouvements_recents = MouvementStock.objects.select_related(
        'stock__produit', 'stock__projet', 'effectue_par'
    ).order_by('-date_mouvement')[:10]
    
    # Statistiques par projet
    stats_projets = Stock.objects.values(
        'projet__code_projet', 'projet__nom_projet'
    ).annotate(
        nb_produits=Count('id'),
        valeur_totale=Sum('valeur_stock')
    ).order_by('-valeur_totale')[:5]
    
    context = {
        'total_produits': total_produits,
        'total_stocks': total_stocks,
        'valeur_totale': valeur_totale,
        'stocks_faibles': stocks_faibles,
        'achats_recents': achats_recents,
        'mouvements_recents': mouvements_recents,
        'stats_projets': stats_projets,
    }
    
    return render(request, 'inventory/dashboard.html', context)


# ============ PRODUITS ============

@login_required
def produit_list(request):
    """Liste des produits"""
    produits = Produit.objects.select_related('categorie', 'unite_mesure').filter(actif=True)
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        produits = produits.filter(
            Q(nom__icontains=search) | 
            Q(code_produit__icontains=search) |
            Q(description__icontains=search)
        )
    
    # Filtrage par catégorie
    categorie_id = request.GET.get('categorie', '')
    if categorie_id:
        produits = produits.filter(categorie_id=categorie_id)
    
    # Pagination
    paginator = Paginator(produits, 20)
    page = request.GET.get('page')
    produits = paginator.get_page(page)
    
    categories = CategorieProduit.objects.filter(actif=True)
    
    context = {
        'produits': produits,
        'categories': categories,
        'search': search,
        'categorie_id': categorie_id,
    }
    
    return render(request, 'inventory/produit_list.html', context)


@login_required
def produit_detail(request, pk):
    """Détail d'un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    # Stocks par projet
    stocks = Stock.objects.filter(produit=produit).select_related('projet')
    
    # Mouvements récents
    mouvements = MouvementStock.objects.filter(
        stock__produit=produit
    ).select_related('stock__projet', 'effectue_par').order_by('-date_mouvement')[:20]
    
    # Achats récents
    achats = LigneAchat.objects.filter(
        produit=produit
    ).select_related('achat__projet', 'achat__fournisseur').order_by('-achat__date_achat')[:10]
    
    context = {
        'produit': produit,
        'stocks': stocks,
        'mouvements': mouvements,
        'achats': achats,
    }
    
    return render(request, 'inventory/produit_detail.html', context)


@login_required
def produit_create(request):
    """Créer un produit"""
    if request.method == 'POST':
        form = ProduitForm(request.POST)
        if form.is_valid():
            produit = form.save()
            messages.success(request, f'Produit {produit.nom} créé avec succès.')
            return redirect('inventory:produit_detail', pk=produit.pk)
    else:
        form = ProduitForm()
    
    context = {'form': form, 'title': 'Nouveau produit'}
    return render(request, 'inventory/produit_form.html', context)


@login_required
def produit_update(request, pk):
    """Modifier un produit"""
    produit = get_object_or_404(Produit, pk=pk)
    
    if request.method == 'POST':
        form = ProduitForm(request.POST, instance=produit)
        if form.is_valid():
            form.save()
            messages.success(request, f'Produit {produit.nom} modifié avec succès.')
            return redirect('inventory:produit_detail', pk=produit.pk)
    else:
        form = ProduitForm(instance=produit)
    
    context = {'form': form, 'produit': produit, 'title': 'Modifier le produit'}
    return render(request, 'inventory/produit_form.html', context)


# ============ STOCKS ============

@login_required
def stock_list(request):
    """Liste des stocks"""
    stocks = Stock.objects.select_related('produit', 'projet', 'produit__unite_mesure')
    
    # Filtrage
    filter_form = StockFilterForm(request.GET)
    if filter_form.is_valid():
        projet = filter_form.cleaned_data.get('projet')
        categorie = filter_form.cleaned_data.get('categorie')
        stock_faible = filter_form.cleaned_data.get('stock_faible')
        
        if projet:
            stocks = stocks.filter(projet=projet)
        if categorie:
            stocks = stocks.filter(produit__categorie=categorie)
        if stock_faible:
            stocks = stocks.filter(quantite_actuelle__lt=F('produit__stock_minimum'))
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        stocks = stocks.filter(
            Q(produit__nom__icontains=search) |
            Q(produit__code_produit__icontains=search) |
            Q(projet__nom_projet__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(stocks, 20)
    page = request.GET.get('page')
    stocks = paginator.get_page(page)
    
    context = {
        'stocks': stocks,
        'filter_form': filter_form,
        'search': search,
    }
    
    return render(request, 'inventory/stock_list.html', context)


@login_required
def stock_detail(request, pk):
    """Détail d'un stock"""
    stock = get_object_or_404(Stock.objects.select_related('produit', 'projet'), pk=pk)
    
    # Mouvements
    mouvements = stock.mouvements.select_related('effectue_par').order_by('-date_mouvement')[:50]
    
    context = {
        'stock': stock,
        'mouvements': mouvements,
    }
    
    return render(request, 'inventory/stock_detail.html', context)


@login_required
def stock_create(request):
    """Créer un stock"""
    if request.method == 'POST':
        form = StockForm(request.POST)
        if form.is_valid():
            stock = form.save()
            stock.calculer_valeur_stock()
            stock.save()
            messages.success(request, 'Stock créé avec succès.')
            return redirect('inventory:stock_detail', pk=stock.pk)
    else:
        form = StockForm()
    
    context = {'form': form, 'title': 'Nouveau stock'}
    return render(request, 'inventory/stock_form.html', context)


# ============ ACHATS ============

@login_required
def achat_list(request):
    """Liste des achats"""
    achats = Achat.objects.select_related('projet', 'fournisseur', 'saisi_par')
    
    # Filtrage
    filter_form = AchatFilterForm(request.GET)
    if filter_form.is_valid():
        projet = filter_form.cleaned_data.get('projet')
        fournisseur = filter_form.cleaned_data.get('fournisseur')
        statut = filter_form.cleaned_data.get('statut')
        date_debut = filter_form.cleaned_data.get('date_debut')
        date_fin = filter_form.cleaned_data.get('date_fin')
        
        if projet:
            achats = achats.filter(projet=projet)
        if fournisseur:
            achats = achats.filter(fournisseur=fournisseur)
        if statut:
            achats = achats.filter(statut=statut)
        if date_debut:
            achats = achats.filter(date_achat__gte=date_debut)
        if date_fin:
            achats = achats.filter(date_achat__lte=date_fin)
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        achats = achats.filter(
            Q(numero_achat__icontains=search) |
            Q(numero_facture__icontains=search) |
            Q(fournisseur__nom__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(achats, 20)
    page = request.GET.get('page')
    achats = paginator.get_page(page)
    
    context = {
        'achats': achats,
        'filter_form': filter_form,
        'search': search,
    }
    
    return render(request, 'inventory/achat_list.html', context)


@login_required
def achat_detail(request, pk):
    """Détail d'un achat"""
    achat = get_object_or_404(
        Achat.objects.select_related('projet', 'fournisseur', 'saisi_par', 'valide_par'),
        pk=pk
    )
    
    # Lignes d'achat
    lignes = achat.lignes.select_related('produit', 'produit__unite_mesure')
    
    context = {
        'achat': achat,
        'lignes': lignes,
    }
    
    return render(request, 'inventory/achat_detail.html', context)


@login_required
def achat_create(request):
    """Créer un achat"""
    if request.method == 'POST':
        form = AchatForm(request.POST, request.FILES)
        formset = LigneAchatFormSet(request.POST)
        
        if form.is_valid() and formset.is_valid():
            achat = form.save(commit=False)
            achat.saisi_par = request.user
            achat.save()
            
            # Sauvegarder les lignes
            lignes = formset.save(commit=False)
            for ligne in lignes:
                ligne.achat = achat
                ligne.save()
            
            # Recalculer le montant total
            achat.calculer_montant_total()
            achat.save()
            
            messages.success(request, f'Achat {achat.numero_achat} créé avec succès.')
            return redirect('inventory:achat_detail', pk=achat.pk)
    else:
        form = AchatForm()
        formset = LigneAchatFormSet()
    
    context = {
        'form': form,
        'formset': formset,
        'title': 'Nouvel achat'
    }
    
    return render(request, 'inventory/achat_form.html', context)


@login_required
def achat_update(request, pk):
    """Modifier un achat"""
    achat = get_object_or_404(Achat, pk=pk)
    
    if achat.statut == 'Reçu':
        messages.error(request, 'Impossible de modifier un achat déjà reçu.')
        return redirect('inventory:achat_detail', pk=achat.pk)
    
    if request.method == 'POST':
        form = AchatForm(request.POST, request.FILES, instance=achat)
        formset = LigneAchatFormSet(request.POST, instance=achat)
        
        if form.is_valid() and formset.is_valid():
            form.save()
            formset.save()
            
            # Recalculer le montant total
            achat.calculer_montant_total()
            achat.save()
            
            messages.success(request, f'Achat {achat.numero_achat} modifié avec succès.')
            return redirect('inventory:achat_detail', pk=achat.pk)
    else:
        form = AchatForm(instance=achat)
        formset = LigneAchatFormSet(instance=achat)
    
    context = {
        'form': form,
        'formset': formset,
        'achat': achat,
        'title': 'Modifier l\'achat'
    }
    
    return render(request, 'inventory/achat_form.html', context)


@login_required
def achat_valider(request, pk):
    """Valider un achat"""
    achat = get_object_or_404(Achat, pk=pk)
    
    if achat.statut != 'Brouillon':
        messages.error(request, 'Seuls les achats en brouillon peuvent être validés.')
        return redirect('inventory:achat_detail', pk=achat.pk)
    
    achat.statut = 'Validé'
    achat.valide_par = request.user
    achat.date_validation = timezone.now()
    achat.save()
    
    messages.success(request, f'Achat {achat.numero_achat} validé avec succès.')
    return redirect('inventory:achat_detail', pk=achat.pk)


@login_required
def achat_recevoir(request, pk):
    """Marquer un achat comme reçu et mettre à jour les stocks"""
    achat = get_object_or_404(Achat, pk=pk)
    
    if achat.statut != 'Validé':
        messages.error(request, 'Seuls les achats validés peuvent être reçus.')
        return redirect('inventory:achat_detail', pk=achat.pk)
    
    # Mettre à jour les stocks pour chaque ligne
    for ligne in achat.lignes.all():
        # Récupérer ou créer le stock
        stock, created = Stock.objects.get_or_create(
            projet=achat.projet,
            produit=ligne.produit,
            defaults={'quantite_actuelle': 0}
        )
        
        # Créer le mouvement de stock
        mouvement = MouvementStock.objects.create(
            stock=stock,
            type_mouvement='Entrée',
            quantite=ligne.quantite,
            achat=achat,
            motif=f'Réception achat {achat.numero_achat}',
            effectue_par=request.user
        )
        
        # Mettre à jour le prix unitaire moyen du produit
        total_quantite = ligne.produit.get_stock_total()
        if total_quantite > 0:
            valeur_actuelle = ligne.produit.prix_unitaire_moyen * Decimal(str(total_quantite - ligne.quantite))
            valeur_nouvelle = ligne.prix_unitaire * ligne.quantite
            ligne.produit.prix_unitaire_moyen = (valeur_actuelle + valeur_nouvelle) / Decimal(str(total_quantite))
            ligne.produit.save()
    
    # Marquer l'achat comme reçu
    achat.statut = 'Reçu'
    achat.date_reception = timezone.now().date()
    achat.save()
    
    messages.success(request, f'Achat {achat.numero_achat} reçu et stocks mis à jour.')
    return redirect('inventory:achat_detail', pk=achat.pk)


# ============ MOUVEMENTS DE STOCK ============

@login_required
def mouvement_list(request):
    """Liste des mouvements de stock"""
    mouvements = MouvementStock.objects.select_related(
        'stock__produit', 'stock__projet', 'effectue_par'
    )
    
    # Filtrage
    type_mouvement = request.GET.get('type_mouvement', '')
    if type_mouvement:
        mouvements = mouvements.filter(type_mouvement=type_mouvement)
    
    projet_id = request.GET.get('projet', '')
    if projet_id:
        mouvements = mouvements.filter(stock__projet_id=projet_id)
    
    # Recherche
    search = request.GET.get('search', '')
    if search:
        mouvements = mouvements.filter(
            Q(stock__produit__nom__icontains=search) |
            Q(motif__icontains=search)
        )
    
    # Pagination
    paginator = Paginator(mouvements, 50)
    page = request.GET.get('page')
    mouvements = paginator.get_page(page)
    
    projets = Projet.objects.filter(statut__in=['Planifié', 'En_cours'])
    
    context = {
        'mouvements': mouvements,
        'projets': projets,
        'type_mouvement': type_mouvement,
        'projet_id': projet_id,
        'search': search,
    }
    
    return render(request, 'inventory/mouvement_list.html', context)


@login_required
def mouvement_create(request):
    """Créer un mouvement de stock"""
    if request.method == 'POST':
        form = MouvementStockForm(request.POST)
        if form.is_valid():
            mouvement = form.save(commit=False)
            mouvement.effectue_par = request.user
            
            # Validation pour les transferts
            if mouvement.type_mouvement == 'Transfert' and not mouvement.projet_destination:
                messages.error(request, 'Le projet de destination est obligatoire pour un transfert.')
                return render(request, 'inventory/mouvement_form.html', {'form': form, 'title': 'Nouveau mouvement'})
            
            # Validation de la quantité pour les sorties
            if mouvement.type_mouvement in ['Sortie', 'Transfert']:
                if mouvement.quantite > mouvement.stock.quantite_actuelle:
                    messages.error(request, 'Quantité insuffisante en stock.')
                    return render(request, 'inventory/mouvement_form.html', {'form': form, 'title': 'Nouveau mouvement'})
            
            mouvement.save()
            
            # Pour les transferts, créer une entrée dans le projet destination
            if mouvement.type_mouvement == 'Transfert' and mouvement.projet_destination:
                stock_dest, created = Stock.objects.get_or_create(
                    projet=mouvement.projet_destination,
                    produit=mouvement.stock.produit,
                    defaults={'quantite_actuelle': 0}
                )
                
                MouvementStock.objects.create(
                    stock=stock_dest,
                    type_mouvement='Entrée',
                    quantite=mouvement.quantite,
                    motif=f'Transfert depuis {mouvement.stock.projet.code_projet}',
                    effectue_par=request.user
                )
            
            messages.success(request, 'Mouvement de stock enregistré avec succès.')
            return redirect('inventory:stock_detail', pk=mouvement.stock.pk)
    else:
        form = MouvementStockForm()
    
    context = {'form': form, 'title': 'Nouveau mouvement'}
    return render(request, 'inventory/mouvement_form.html', context)


# ============ ALERTES ============

@login_required
def alertes_stock(request):
    """Page des alertes de stock faible"""
    # Stocks faibles par projet
    stocks_faibles = Stock.objects.select_related(
        'produit', 'projet', 'produit__unite_mesure'
    ).filter(
        quantite_actuelle__lt=F('produit__stock_minimum')
    ).order_by('projet', 'quantite_actuelle')
    
    # Grouper par projet
    alertes_par_projet = {}
    for stock in stocks_faibles:
        projet_code = stock.projet.code_projet
        if projet_code not in alertes_par_projet:
            alertes_par_projet[projet_code] = {
                'projet': stock.projet,
                'stocks': []
            }
        alertes_par_projet[projet_code]['stocks'].append(stock)
    
    context = {
        'alertes_par_projet': alertes_par_projet,
        'total_alertes': stocks_faibles.count(),
    }
    
    return render(request, 'inventory/alertes_stock.html', context)
