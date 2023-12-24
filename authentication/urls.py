from django.urls import path, include
from . import views


urlpatterns = [
    path('registration/', views.registrationView, name='registration'),
    path('login/', views.loginView, name='login'),
    path('edit/', views.editView, name='edit'),
    path('change-password/', views.ChangePasswordView.as_view(), name='change-password'),
    path('delete-avatar/', views.deleteAvatar, name='delete-avatar'),
    path('logout/', views.logoutView, name='logout'),
]