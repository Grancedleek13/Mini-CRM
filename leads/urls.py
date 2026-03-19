from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new/', views.create_lead, name='create_lead'),
    path('lead/<int:lead_id>/status/', views.update_status, name='update_status'),
    path('api/leads/', views.api_leads, name='api_leads'),
    path('api/leads/<int:lead_id>/', views.api_lead_detail, name='api_lead_detail'),
]
