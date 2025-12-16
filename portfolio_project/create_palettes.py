import os
import sys

# Aggiungi il path del progetto  
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'portfolio_project.settings')

import django
django.setup()

from portfolio.models import ColorPalette, SiteSettings

# Palette moderne e professionali - 2025
palettes = [
    {
        'name': 'Minimal Dark',
        'primary_color': '#0f172a',      # Slate dark
        'secondary_color': '#1e293b',    # Slate medium
        'accent_color': '#06b6d4',       # Cyan bright
        'background_color': '#ffffff',
        'text_color': '#0f172a',
        'is_active': True
    },
    {
        'name': 'Professional Blue',
        'primary_color': '#1e40af',      # Blue professional
        'secondary_color': '#3b82f6',    # Blue bright
        'accent_color': '#f59e0b',       # Amber accent
        'background_color': '#f8fafc',   # Slate lightest
        'text_color': '#1e293b',
        'is_active': False
    },
    {
        'name': 'Elegant Gray',
        'primary_color': '#374151',      # Gray dark
        'secondary_color': '#6b7280',    # Gray medium
        'accent_color': '#8b5cf6',       # Violet accent
        'background_color': '#f9fafb',
        'text_color': '#111827',
        'is_active': False
    },
    {
        'name': 'Nordic Light',
        'primary_color': '#0891b2',      # Cyan dark
        'secondary_color': '#06b6d4',    # Cyan bright
        'accent_color': '#ec4899',       # Pink accent
        'background_color': '#fefefe',
        'text_color': '#0f172a',
        'is_active': False
    },
    {
        'name': 'Sophisticated Navy',
        'primary_color': '#1e3a8a',      # Blue dark navy
        'secondary_color': '#2563eb',    # Blue medium
        'accent_color': '#14b8a6',       # Teal accent
        'background_color': '#f8fafc',
        'text_color': '#0f172a',
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
