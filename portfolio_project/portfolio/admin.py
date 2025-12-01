from django.contrib import admin
from django.utils.html import format_html
from .models import ColorPalette, Project, Skill, Experience, ContactMessage, SiteSettings


@admin.register(ColorPalette)
class ColorPaletteAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle palette colori.
    """
    list_display = ['name', 'color_preview', 'is_active', 'created_at']
    list_filter = ['is_active']
    search_fields = ['name']
    list_editable = ['is_active']
    
    fieldsets = (
        ('Informazioni', {
            'fields': ('name', 'is_active')
        }),
        ('Colori', {
            'fields': (
                'primary_color', 
                'secondary_color', 
                'accent_color', 
                'text_color', 
                'background_color'
            ),
            'description': 'Inserire i colori in formato esadecimale (es. #007bff)'
        }),
    )
    
    def color_preview(self, obj):
        """Mostra un'anteprima dei colori della palette."""
        return format_html(
            '''
            <div style="display: flex; gap: 5px;">
                <span style="background-color: {}; width: 25px; height: 25px; display: inline-block; border: 1px solid #ccc; border-radius: 3px;" title="Primary"></span>
                <span style="background-color: {}; width: 25px; height: 25px; display: inline-block; border: 1px solid #ccc; border-radius: 3px;" title="Secondary"></span>
                <span style="background-color: {}; width: 25px; height: 25px; display: inline-block; border: 1px solid #ccc; border-radius: 3px;" title="Accent"></span>
                <span style="background-color: {}; width: 25px; height: 25px; display: inline-block; border: 1px solid #ccc; border-radius: 3px;" title="Text"></span>
                <span style="background-color: {}; width: 25px; height: 25px; display: inline-block; border: 1px solid #ccc; border-radius: 3px;" title="Background"></span>
            </div>
            ''',
            obj.primary_color,
            obj.secondary_color,
            obj.accent_color,
            obj.text_color,
            obj.background_color
        )
    color_preview.short_description = 'Anteprima'


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    """
    Admin per la gestione dei progetti.
    """
    list_display = ['title', 'category', 'featured', 'order', 'created_at']
    list_filter = ['category', 'featured', 'created_at']
    search_fields = ['title', 'description', 'technologies']
    list_editable = ['featured', 'order']
    prepopulated_fields = {'slug': ('title',)}
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Informazioni Principali', {
            'fields': ('title', 'slug', 'short_description', 'description')
        }),
        ('Media', {
            'fields': ('image',)
        }),
        ('Dettagli Tecnici', {
            'fields': ('technologies', 'category')
        }),
        ('Link', {
            'fields': ('project_url', 'github_url')
        }),
        ('Visibilità', {
            'fields': ('featured', 'order')
        }),
    )


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle skill.
    """
    list_display = ['name', 'category', 'proficiency_stars', 'icon_preview', 'order']
    list_filter = ['category', 'proficiency']
    search_fields = ['name']
    list_editable = ['order']
    
    def proficiency_stars(self, obj):
        """Mostra il livello come stelle."""
        stars = '★' * obj.proficiency + '☆' * (5 - obj.proficiency)
        return format_html('<span style="color: #ffc107;">{}</span>', stars)
    proficiency_stars.short_description = 'Livello'
    
    def icon_preview(self, obj):
        """Mostra l'icona FontAwesome."""
        return format_html('<i class="{}"></i> {}', obj.icon, obj.icon)
    icon_preview.short_description = 'Icona'


@admin.register(Experience)
class ExperienceAdmin(admin.ModelAdmin):
    """
    Admin per la gestione delle esperienze.
    """
    list_display = ['title', 'company', 'location', 'start_date', 'end_date', 'is_current', 'order']
    list_filter = ['is_current', 'start_date']
    search_fields = ['title', 'company', 'description']
    list_editable = ['order']
    date_hierarchy = 'start_date'
    
    fieldsets = (
        ('Posizione', {
            'fields': ('title', 'company', 'location')
        }),
        ('Periodo', {
            'fields': ('start_date', 'end_date', 'is_current')
        }),
        ('Descrizione', {
            'fields': ('description',)
        }),
        ('Ordinamento', {
            'fields': ('order',)
        }),
    )


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    """
    Admin per la visualizzazione dei messaggi di contatto.
    """
    list_display = ['subject', 'name', 'email', 'created_at', 'is_read']
    list_filter = ['is_read', 'created_at']
    search_fields = ['name', 'email', 'subject', 'message']
    readonly_fields = ['name', 'email', 'subject', 'message', 'created_at']
    list_editable = ['is_read']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Mittente', {
            'fields': ('name', 'email')
        }),
        ('Messaggio', {
            'fields': ('subject', 'message')
        }),
        ('Stato', {
            'fields': ('created_at', 'is_read')
        }),
    )
    
    def has_add_permission(self, request):
        """Disabilita l'aggiunta manuale di messaggi."""
        return False


@admin.register(SiteSettings)
class SiteSettingsAdmin(admin.ModelAdmin):
    """
    Admin per le impostazioni del sito.
    """
    fieldsets = (
        ('Informazioni Sito', {
            'fields': ('site_title', 'site_description')
        }),
        ('Autore', {
            'fields': ('author_name', 'author_bio', 'author_image')
        }),
        ('Contatti', {
            'fields': ('email', 'phone', 'location')
        }),
        ('Social', {
            'fields': ('social_links',),
            'description': 'Inserire i link social in formato JSON: {"github": "url", "linkedin": "url"}'
        }),
        ('Tema', {
            'fields': ('current_palette',)
        }),
    )
    
    def has_add_permission(self, request):
        """Limita a una sola istanza."""
        return not SiteSettings.objects.exists()
    
    def has_delete_permission(self, request, obj=None):
        """Impedisce l'eliminazione delle impostazioni."""
        return False


# Personalizzazione dell'admin
admin.site.site_header = 'Portfolio Admin'
admin.site.site_title = 'Portfolio Admin'
admin.site.index_title = 'Gestione Portfolio'
