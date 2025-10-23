from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import CustomAuthenticationForm, UserRegistrationForm, UserUpdateForm, ProfileUpdateForm

User = get_user_model()


def login_view(request):
    """Vue de connexion"""
    if request.user.is_authenticated:
        return redirect('core:home')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                if user.actif:
                    login(request, user)
                    user.derniere_connexion = timezone.now()
                    user.save(update_fields=['derniere_connexion'])
                    messages.success(request, f'Bienvenue {user.get_full_name()}!')
                    return redirect('core:home')
                else:
                    messages.error(request, 'Votre compte est désactivé.')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'accounts/login.html', {'form': form})


@login_required
def logout_view(request):
    """Vue de déconnexion"""
    logout(request)
    messages.info(request, 'Vous avez été déconnecté avec succès.')
    return redirect('accounts:login')


@login_required
def profile_view(request):
    """Vue du profil utilisateur"""
    return render(request, 'accounts/profile.html', {'user': request.user})


@login_required
def profile_update_view(request):
    """Vue de mise à jour du profil"""
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Votre profil a été mis à jour avec succès.')
            return redirect('accounts:profile')
    else:
        form = ProfileUpdateForm(instance=request.user)
    
    return render(request, 'accounts/profile_update.html', {'form': form})


class AdminRequiredMixin(UserPassesTestMixin):
    """Mixin pour vérifier que l'utilisateur est admin"""
    def test_func(self):
        return self.request.user.is_admin()


class UserListView(LoginRequiredMixin, AdminRequiredMixin, ListView):
    """Liste des utilisateurs"""
    model = User
    template_name = 'accounts/user_list.html'
    context_object_name = 'users'
    paginate_by = 20
    
    def get_queryset(self):
        queryset = User.objects.all().order_by('-date_joined')
        search = self.request.GET.get('search')
        if search:
            queryset = queryset.filter(
                username__icontains=search
            ) | queryset.filter(
                first_name__icontains=search
            ) | queryset.filter(
                last_name__icontains=search
            ) | queryset.filter(
                email__icontains=search
            )
        return queryset


class UserDetailView(LoginRequiredMixin, AdminRequiredMixin, DetailView):
    """Détails d'un utilisateur"""
    model = User
    template_name = 'accounts/user_detail.html'
    context_object_name = 'user_obj'


class UserCreateView(LoginRequiredMixin, AdminRequiredMixin, CreateView):
    """Création d'un utilisateur"""
    model = User
    form_class = UserRegistrationForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur créé avec succès.')
        return super().form_valid(form)


class UserUpdateView(LoginRequiredMixin, AdminRequiredMixin, UpdateView):
    """Mise à jour d'un utilisateur"""
    model = User
    form_class = UserUpdateForm
    template_name = 'accounts/user_form.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def form_valid(self, form):
        messages.success(self.request, 'Utilisateur mis à jour avec succès.')
        return super().form_valid(form)


class UserDeleteView(LoginRequiredMixin, AdminRequiredMixin, DeleteView):
    """Suppression d'un utilisateur"""
    model = User
    template_name = 'accounts/user_confirm_delete.html'
    success_url = reverse_lazy('accounts:user_list')
    
    def delete(self, request, *args, **kwargs):
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return super().delete(request, *args, **kwargs)
