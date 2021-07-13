from django.urls import path
from . import views
urlpatterns = [
    path('user-register/', views.user_register),
    path('user-risk/', views.user_risk),
    path('admin-register/', views.admin_register),
    path('admin-report/', views.admin_report),
]
