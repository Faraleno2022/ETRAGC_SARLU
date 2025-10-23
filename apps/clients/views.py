from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.urls import reverse_lazy
from django.db.models import Q
from .models import Client
from .forms import ClientForm


class ClientListView(LoginRequiredMixin, ListView):
    """Liste des clients"""
    model = Client
    template_name = 'clients/client_list.html'
    context_object_name = 'clients'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = Client.objects.all()
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                Q(nom_complet__icontains=search) |
                Q(entreprise__icontains=search) |
                Q(email__icontains=search) |
                Q(telephone__icontains=search)
            )
        return queryset


class ClientDetailView(LoginRequiredMixin, DetailView):
    """Détails d'un client"""
    model = Client
    template_name = 'clients/client_detail.html'
    context_object_name = 'client'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['projets'] = self.object.projets.all()
        return context


class ClientCreateView(LoginRequiredMixin, CreateView):
    """Création d'un client"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Client créé avec succès.')
        return super().form_valid(form)


class ClientUpdateView(LoginRequiredMixin, UpdateView):
    """Mise à jour d'un client"""
    model = Client
    form_class = ClientForm
    template_name = 'clients/client_form.html'
    success_url = reverse_lazy('clients:list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Client mis à jour avec succès.')
        return super().form_valid(form)


class ClientDeleteView(LoginRequiredMixin, DeleteView):
    """Suppression d'un client"""
    model = Client
    template_name = 'clients/client_confirm_delete.html'
    success_url = reverse_lazy('clients:list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Client supprimé avec succès.')
        return super().delete(request, *args, **kwargs)
