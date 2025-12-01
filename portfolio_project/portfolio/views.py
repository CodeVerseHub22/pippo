from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import Project, Skill, Experience, ColorPalette, SiteSettings, ContactMessage
from .forms import ContactForm


def index(request):
    """
    Home page del portfolio.
    Mostra progetti in evidenza e skill principali.
    """
    featured_projects = Project.objects.filter(featured=True)[:6]
    skills = Skill.objects.all()[:12]
    
    # Raggruppa le skill per categoria
    skills_by_category = {}
    for skill in Skill.objects.all():
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    context = {
        'featured_projects': featured_projects,
        'skills': skills,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'home.html', context)


def projects_list(request):
    """
    Lista di tutti i progetti con filtri per categoria.
    """
    projects = Project.objects.all()
    
    # Filtro per categoria
    category = request.GET.get('category')
    if category and category != 'all':
        projects = projects.filter(category=category)
    
    # Paginazione
    paginator = Paginator(projects, 9)  # 9 progetti per pagina
    page = request.GET.get('page')
    projects = paginator.get_page(page)
    
    # Categorie disponibili per il filtro
    categories = Project.CATEGORY_CHOICES
    
    context = {
        'projects': projects,
        'categories': categories,
        'current_category': category or 'all',
    }
    return render(request, 'projects.html', context)


def project_detail(request, slug):
    """
    Dettagli di un singolo progetto.
    """
    project = get_object_or_404(Project, slug=slug)
    
    # Progetti correlati (stessa categoria, escluso quello corrente)
    related_projects = Project.objects.filter(
        category=project.category
    ).exclude(pk=project.pk)[:3]
    
    context = {
        'project': project,
        'related_projects': related_projects,
    }
    return render(request, 'project_detail.html', context)


def about(request):
    """
    Pagina Chi Sono con bio, esperienze e skill.
    """
    experiences = Experience.objects.all()
    skills = Skill.objects.all()
    
    # Raggruppa le skill per categoria
    skills_by_category = {}
    for skill in skills:
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)
    
    context = {
        'experiences': experiences,
        'skills_by_category': skills_by_category,
    }
    return render(request, 'about.html', context)


def contact(request):
    """
    Form di contatto.
    """
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            # Salva il messaggio
            contact_message = form.save()
            
            # Invia email di notifica (in produzione)
            try:
                site_settings = SiteSettings.get_settings()
                if site_settings.email:
                    send_mail(
                        subject=f"Nuovo messaggio: {contact_message.subject}",
                        message=f"Da: {contact_message.name} ({contact_message.email})\n\n{contact_message.message}",
                        from_email=django_settings.DEFAULT_FROM_EMAIL if hasattr(django_settings, 'DEFAULT_FROM_EMAIL') else None,
                        recipient_list=[site_settings.email],
                        fail_silently=True,
                    )
            except Exception:
                pass  # Silently fail if email sending fails
            
            messages.success(request, 'Messaggio inviato con successo!')
            return redirect('contact_success')
    else:
        form = ContactForm()
    
    context = {
        'form': form,
    }
    return render(request, 'contact.html', context)


def contact_success(request):
    """
    Pagina di conferma invio messaggio.
    """
    return render(request, 'success.html')


def get_active_palette(request):
    """
    API endpoint per ottenere la palette colori attiva.
    """
    palette = ColorPalette.objects.filter(is_active=True).first()
    
    if palette:
        data = {
            'name': palette.name,
            'primary_color': palette.primary_color,
            'secondary_color': palette.secondary_color,
            'accent_color': palette.accent_color,
            'text_color': palette.text_color,
            'background_color': palette.background_color,
        }
    else:
        # Palette di default
        data = {
            'name': 'Default',
            'primary_color': '#007bff',
            'secondary_color': '#6c757d',
            'accent_color': '#28a745',
            'text_color': '#212529',
            'background_color': '#ffffff',
        }
    
    return JsonResponse(data)


def get_skills_api(request):
    """
    API endpoint per ottenere tutte le skill in formato JSON.
    """
    skills = Skill.objects.all()
    data = []
    
    for skill in skills:
        data.append({
            'name': skill.name,
            'category': skill.category,
            'category_display': skill.get_category_display(),
            'proficiency': skill.proficiency,
            'icon': skill.icon,
        })
    
    return JsonResponse({'skills': data})


def custom_404(request, exception):
    """
    Pagina di errore 404 personalizzata.
    """
    return render(request, '404.html', status=404)


def custom_500(request):
    """
    Pagina di errore 500 personalizzata.
    """
    return render(request, '500.html', status=500)
