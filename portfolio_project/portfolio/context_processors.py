from .models import SiteSettings, ColorPalette


def site_settings(request):
    """
    Context processor per rendere disponibili le impostazioni del sito
    in tutti i template.
    """
    settings = SiteSettings.get_settings()
    
    # Ottieni la palette attiva
    palette = None
    if settings.current_palette:
        palette = settings.current_palette
    else:
        # Cerca una palette attiva
        palette = ColorPalette.objects.filter(is_active=True).first()
    
    return {
        'site_settings': settings,
        'active_palette': palette,
    }
