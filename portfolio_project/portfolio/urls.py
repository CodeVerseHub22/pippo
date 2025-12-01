from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path('', views.index, name='home'),
    path('projects/', views.projects_list, name='projects'),
    path('projects/<slug:slug>/', views.project_detail, name='project_detail'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact/success/', views.contact_success, name='contact_success'),
    
    # API endpoints
    path('api/palette/', views.get_active_palette, name='api_palette'),
    path('api/skills/', views.get_skills_api, name='api_skills'),
]
