import os
import sys

# Aggiungi il path del progetto
sys.path.insert(0, r'c:\Users\Postazione16Aula1\Desktop\Portfolio\portfolio_project')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

import django
django.setup()

from portfolio.models import ColorPalette, SiteSettings

# Crea palette predefinite
palettes = [
    {
        'name': 'Modern Blue',
        'primary_color': '#3498db',
        'secondary_color': '#2980b9',
        'accent_color': '#e74c3c',
        'background_color': '#f8f9fa',
        'text_color': '#2c3e50',
        'is_active': True
    },
    {
        'name': 'Forest Green',
        'primary_color': '#27ae60',
        'secondary_color': '#1e8449',
        'accent_color': '#f39c12',
        'background_color': '#f5f5f5',
        'text_color': '#2d3436',
        'is_active': False
    },
    {
        'name': 'Royal Purple',
        'primary_color': '#9b59b6',
        'secondary_color': '#8e44ad',
        'accent_color': '#e67e22',
        'background_color': '#fafafa',
        'text_color': '#34495e',
        'is_active': False
    },
    {
        'name': 'Sunset Orange',
        'primary_color': '#e74c3c',
        'secondary_color': '#c0392b',
        'accent_color': '#3498db',
        'background_color': '#fff5f5',
        'text_color': '#2c3e50',
        'is_active': False
    },
    {
        'name': 'Ocean Teal',
        'primary_color': '#1abc9c',
        'secondary_color': '#16a085',
        'accent_color': '#e74c3c',
        'background_color': '#f0ffff',
        'text_color': '#2c3e50',
        'is_active': False
    },
]

print("Creazione palette colori...")
for p in palettes:
    obj, created = ColorPalette.objects.update_or_create(
        name=p['name'],
        defaults=p
    )
    status = 'Creata' if created else 'Aggiornata'
    print(f"  {status}: {p['name']}")

# Assicurati che ci sia un SiteSettings
print("\nConfigurazione impostazioni sito...")
settings = SiteSettings.get_settings()
settings.site_title = 'Il Mio Portfolio'
settings.author_name = 'Developer'
settings.site_description = 'Portfolio professionale di uno sviluppatore web'
settings.save()
print("Impostazioni salvate!")

print("\nPalette disponibili:")
for palette in ColorPalette.objects.all():
    print(f"  - {palette.name} {'(ATTIVA)' if palette.is_active else ''}")
