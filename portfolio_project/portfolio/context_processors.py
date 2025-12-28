from .models import SiteSettings


def site_settings(request):
    """
    Context processor per rendere disponibili le impostazioni del sito
    in tutti i template.
    """
    settings = SiteSettings.get_settings()
    
    return {
        'site_settings': settings,
    }
