from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings as django_settings
from .models import Project, Skill, Experience, SiteSettings, Education, Certification
from .forms import ContactForm


def index(request):
    """
    Home page del portfolio.
    Mostra progetti in evidenza, skill, esperienze, formazione.
    """
    featured_projects = Project.objects.filter(featured=True)[:6]
    skills = Skill.objects.all()[:12]
    experiences = Experience.objects.all().order_by('-start_date')
    education = Education.objects.all().order_by('order')

    # Raggruppa le skill per categoria
    skills_by_category = {}
    for skill in Skill.objects.all():
        category = skill.get_category_display()
        if category not in skills_by_category:
            skills_by_category[category] = []
        skills_by_category[category].append(skill)

    context = {
        "featured_projects": featured_projects,
        "skills": skills,
        "skills_by_category": skills_by_category,
        "experiences": experiences,
        "education": education,
    }
    return render(request, "home.html", context)


def projects_list(request):
    """
    Lista di tutti i progetti con filtri per categoria.
    """
    projects = Project.objects.all()

    # Filtro per categoria
    category = request.GET.get("category")
    if category and category != "all":
        projects = projects.filter(category=category)

    # Paginazione
    paginator = Paginator(projects, 9)  # 9 progetti per pagina
    page = request.GET.get("page")
    projects = paginator.get_page(page)

    # Categorie disponibili per il filtro
    categories = Project.CATEGORY_CHOICES

    context = {
        "projects": projects,
        "categories": categories,
        "current_category": category or "all",
    }
    return render(request, "projects.html", context)


def certifications_list(request):
    """
    Lista di tutte le certificazioni ottenute.
    """
    certifications = Certification.objects.all()

    context = {
        "certifications": certifications,
    }
    return render(request, "certifications.html", context)


def project_detail(request, slug):
    """
    Dettagli di un singolo progetto.
    """
    project = get_object_or_404(Project, slug=slug)

    # Progetti correlati (stessa categoria, escluso quello corrente)
    related_projects = Project.objects.filter(category=project.category).exclude(
        pk=project.pk
    )[:3]

    context = {
        "project": project,
        "related_projects": related_projects,
    }
    return render(request, "project_detail.html", context)


def contact(request):
    """
    Form di contatto.
    """
    if request.method == "POST":
        form = ContactForm(request.POST)
        if form.is_valid():
            # Salva il messaggio
            contact_message = form.save()

            # Invia email di notifica (in produzione)
            try:
                site_settings = SiteSettings.get_settings()
                if site_settings.email:
                    subject = f"Nuovo messaggio: {contact_message.subject}"
                    body = (
                        f"Da: {contact_message.name} "
                        f"({contact_message.email})\n\n"
                        f"{contact_message.message}"
                    )
                    from_email = getattr(django_settings, "DEFAULT_FROM_EMAIL", None)
                    send_mail(
                        subject=subject,
                        message=body,
                        from_email=from_email,
                        recipient_list=[site_settings.email],
                        fail_silently=True,
                    )
            except Exception:
                pass  # Silently fail if email sending fails

            messages.success(request, "Messaggio inviato con successo!")
            return redirect("contact_success")
    else:
        form = ContactForm()

    context = {
        "form": form,
    }
    return render(request, "contact.html", context)


def contact_success(request):
    """
    Pagina di conferma invio messaggio.
    """
    return render(request, "success.html")


def custom_404(request, exception):
    """
    Pagina di errore 404 personalizzata.
    """
    return render(request, "404.html", status=404)


def custom_500(request):
    """
    Pagina di errore 500 personalizzata.
    """
    return render(request, "500.html", status=500)
