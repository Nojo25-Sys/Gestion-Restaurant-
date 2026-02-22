from django.urls import path
from . import views

app_name = 'users'

urlpatterns = [
    # Dashboard
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # Authentification
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
    
    # Gestion des utilisateurs
    path('list/', views.user_list, name='list'),
    path('<int:user_id>/', views.user_detail, name='detail'),
    path('<int:user_id>/update/', views.user_update, name='update'),
    path('<int:user_id>/delete/', views.user_delete, name='delete'),
]
