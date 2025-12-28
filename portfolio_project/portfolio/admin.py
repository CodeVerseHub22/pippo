from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Project,
    Skill,
    Experience,
    Education,
    ContactMessage,
    SiteSettings,
    Certification,
)


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin per la gestione dei progetti.
    """

    list_display = ["title", "category", "featured", "order", "created_at"]
    list_filter = ["category", "featured", "created_at"]
    search_fields = ["title", "description", "technologies"]
    list_editable = ["featured", "order"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "created_at"

    fieldsets = (
        (
            "Informazioni Principali",
            {"fields": ("title", "slug", "short_description", "description")},
        ),
        ("Media", {"fields": ("image",)}),
        ("Dettagli Tecnici", {"fields": ("technologies", "category")}),
        ("Link", {"fields": ("project_url", "github_url")}),
        ("Visibilità", {"fields": ("featured", "order")}),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle skill.
    """

    list_display = ["name", "category", "proficiency_stars", "icon_preview", "order"]
    list_filter = ["category", "proficiency"]
    search_fields = ["name"]
    list_editable = ["order"]

    def proficiency_stars(self, obj):
        """Mostra il livello come stelle."""
        stars = "★" * obj.proficiency + "☆" * (5 - obj.proficiency)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)

    proficiency_stars.short_description = "Livello"

    def icon_preview(self, obj):
        """Mostra l'icona FontAwesome."""
        return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)

    icon_preview.short_description = "Icona"


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle esperienze.
    """

    list_display = [
        "title",
        "company",
        "location",
        "start_date",
        "end_date",
        "is_current",
        "order",
    ]
    list_filter = ["is_current", "start_date"]
    search_fields = ["title", "company", "description"]
    list_editable = ["order"]
    date_hierarchy = "start_date"

    fieldsets = (
        ("Posizione", {"fields": ("title", "company", "location")}),
        ("Periodo", {"fields": ("start_date", "end_date", "is_current")}),
        ("Descrizione", {"fields": ("description", "order")}),
    )


@admin.register(Education)
class EducationAdmin(admin.ModelAdmin):
    """
    Admin per la gestione della formazione.
    """

    list_display = ["title", "institution", "hours", "order"]
    list_filter = ["institution"]
    search_fields = ["title", "institution", "description"]
    list_editable = ["order"]

    fieldsets = (
        ("Informazioni", {"fields": ("title", "institution", "hours")}),
        ("Dettagli", {"fields": ("description", "order")}),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin per la visualizzazione dei messaggi di contatto.
    """

    list_display = ["subject", "name", "email", "created_at", "is_read"]
    list_filter = ["is_read", "created_at"]
    search_fields = ["name", "email", "subject", "message"]
    readonly_fields = ["name", "email", "subject", "message", "created_at"]
    list_editable = ["is_read"]
    date_hierarchy = "created_at"

    fieldsets = (
        ("Mittente", {"fields": ("name", "email")}),
        ("Messaggio", {"fields": ("subject", "message")}),
        ("Stato", {"fields": ("created_at", "is_read")}),
    )

    def has_add_permission(self, request):
        return False


@admin.register(Certification)
class CertificationAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle certificazioni.
    """

    list_display = ["title", "issuing_organization", "issue_date", "order"]
    list_filter = ["issuing_organization", "issue_date"]
    search_fields = ["title", "issuing_organization", "description"]
    list_editable = ["order"]
    date_hierarchy = "issue_date"

    fieldsets = (
        (
            "Informazioni Certificazione",
            {"fields": ("title", "issuing_organization", "issue_date")},
        ),
        ("Media & Link", {"fields": ("certificate_image", "verification_url")}),
        ("Dettagli", {"fields": ("description", "order")}),
    )


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin per le impostazioni del sito.
    """

    fieldsets = (
        ("Informazioni Sito", {"fields": ("site_title", "site_description")}),
        (
            "Autore",
            {"fields": ("author_name", "author_bio", "author_image", "homepage_image", "cv_file")},
        ),
        ("Contatti", {"fields": ("email", "phone", "location")}),
        (
            "Social",
            {"fields": ("social_links",), "description": "Link social in formato JSON"},
        ),
    )

    def has_add_permission(self, request):
        return not SiteSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


admin.site.site_header = "Portfolio Admin"
admin.site.site_title = "Portfolio Admin"
admin.site.index_title = "Gestione Portfolio"
