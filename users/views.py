from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q, Sum, Count
from django.utils import timezone
from .models import User
from .forms import CustomUserCreationForm, CustomAuthenticationForm, UserUpdateForm
from produits_app.models import Produit
from commandes_app.models import Commande

@login_required
def dashboard_view(request):
    """
    Vue principale du dashboard
    """
    # Statistiques pour le dashboard
    produit_count = Produit.objects.count()
    commandes_count = Commande.objects.count()
    
    # Chiffre d'affaires (commandes validées)
    chiffre_affaires = Commande.objects.filter(
        statut__in=['PRETE', 'SERVIE']
    ).aggregate(total=Sum('montant_total'))['total'] or 0
    
    context = {
        'user': request.user,
        'user_count': User.objects.count(),
        'produit_count': produit_count,
        'commandes_count': commandes_count,
        'chiffre_affaires': chiffre_affaires,
    }
    return render(request, 'users/dashboard.html', context)

def login_view(request):
    """
    Vue de connexion
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Bienvenue {username} !')
                return redirect('users:dashboard')
            else:
                messages.error(request, 'Nom d\'utilisateur ou mot de passe incorrect.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'users/login.html', {'form': form})

def logout_view(request):
    """
    Vue de déconnexion
    """
    logout(request)
    messages.info(request, 'Vous avez été déconnecté.')
    return redirect('users:login')

def register_view(request):
    """
    Vue d'inscription
    """
    if request.user.is_authenticated:
        return redirect('users:dashboard')
    
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, 'Compte créé avec succès. Vous pouvez maintenant vous connecter.')
            return redirect('users:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'users/register.html', {'form': form})

@login_required
def user_list(request):
    """
    Liste des utilisateurs (réservé aux admins/managers)
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('users:dashboard')
    
    query = request.GET.get('q', '')
    users = User.objects.all()
    
    if query:
        users = users.filter(
            Q(username__icontains=query) |
            Q(email__icontains=query) |
            Q(first_name__icontains=query) |
            Q(last_name__icontains=query)
        )
    
    return render(request, 'users/list.html', {'users': users, 'query': query})

@login_required
def user_detail(request, user_id):
    """
    Détail d'un utilisateur
    """
    if not request.user.is_manager:
        messages.error(request, 'Accès non autorisé.')
        return redirect('users:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    return render(request, 'users/detail.html', {'user_obj': user})

@login_required
def user_update(request, user_id):
    """
    Mise à jour d'un utilisateur
    """
    if not request.user.is_admin:
        messages.error(request, 'Accès non autorisé.')
        return redirect('users:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Utilisateur mis à jour avec succès.')
            return redirect('users:detail', user_id=user.id)
    else:
        form = UserUpdateForm(instance=user)
    
    return render(request, 'users/update.html', {'form': form, 'user_obj': user})

@login_required
def user_delete(request, user_id):
    """
    Suppression d'un utilisateur
    """
    if not request.user.is_admin:
        messages.error(request, 'Accès non autorisé.')
        return redirect('users:dashboard')
    
    user = get_object_or_404(User, id=user_id)
    
    if user == request.user:
        messages.error(request, 'Vous ne pouvez pas supprimer votre propre compte.')
        return redirect('users:list')
    
    if request.method == 'POST':
        user.delete()
        messages.success(request, 'Utilisateur supprimé avec succès.')
        return redirect('users:list')
    
    return render(request, 'users/delete.html', {'user_obj': user})
