from django.urls import path
from . import views

urlpatterns = [
    # Main pages
    path("", views.index, name="home"),
    path("projects/", views.projects_list, name="projects"),
    path("certifications/", views.certifications_list, name="certifications"),
    path("projects/<slug:slug>/", views.project_detail, name="project_detail"),
    path("contact/", views.contact, name="contact"),
    path("contact/success/", views.contact_success, name="contact_success"),
]
