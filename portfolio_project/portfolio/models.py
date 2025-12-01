from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
import json


class ColorPalette(models.Model):
    """
    Modello per gestire le palette di colori del sito.
    Una sola palette può essere attiva alla volta.
    """
    name = models.CharField(max_length=100, verbose_name="Nome Palette")
    primary_color = models.CharField(
        max_length=7, 
        default='#007bff', 
        verbose_name="Colore Primario",
        help_text="Formato esadecimale (es. #007bff)"
    )
    secondary_color = models.CharField(
        max_length=7, 
        default='#6c757d', 
        verbose_name="Colore Secondario"
    )
    accent_color = models.CharField(
        max_length=7, 
        default='#28a745', 
        verbose_name="Colore Accento"
    )
    text_color = models.CharField(
        max_length=7, 
        default='#212529', 
        verbose_name="Colore Testo"
    )
    background_color = models.CharField(
        max_length=7, 
        default='#ffffff', 
        verbose_name="Colore Sfondo"
    )
    is_active = models.BooleanField(
        default=False, 
        verbose_name="Palette Attiva"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Palette Colori"
        verbose_name_plural = "Palette Colori"
        ordering = ['-is_active', 'name']
    
    def __str__(self):
        active = " (Attiva)" if self.is_active else ""
        return f"{self.name}{active}"
    
    def save(self, *args, **kwargs):
        # Se questa palette è attiva, disattiva tutte le altre
        if self.is_active:
            ColorPalette.objects.exclude(pk=self.pk).update(is_active=False)
        super().save(*args, **kwargs)


class Project(models.Model):
    """
    Modello per i progetti del portfolio.
    """
    CATEGORY_CHOICES = [
        ('web', 'Web Development'),
        ('mobile', 'Mobile Development'),
        ('fullstack', 'Full Stack'),
    ]
    
    title = models.CharField(max_length=200, verbose_name="Titolo")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Descrizione Completa")
    short_description = models.CharField(
        max_length=300, 
        verbose_name="Descrizione Breve"
    )
    image = models.ImageField(
        upload_to='projects/', 
        verbose_name="Immagine Principale",
        blank=True,
        null=True
    )
    technologies = models.CharField(
        max_length=500, 
        verbose_name="Tecnologie",
        help_text="Separare con virgola (es. Python, Django, React)"
    )
    project_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="URL Progetto"
    )
    github_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="URL GitHub"
    )
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='web',
        verbose_name="Categoria"
    )
    featured = models.BooleanField(
        default=False, 
        verbose_name="In Evidenza"
    )
    order = models.IntegerField(
        default=0, 
        verbose_name="Ordine"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
        ordering = ['order', '-created_at']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
    
    def get_technologies_list(self):
        """Restituisce le tecnologie come lista."""
        return [tech.strip() for tech in self.technologies.split(',')]


class Skill(models.Model):
    """
    Modello per le competenze tecniche.
    """
    CATEGORY_CHOICES = [
        ('backend', 'Backend'),
        ('frontend', 'Frontend'),
        ('mobile', 'Mobile'),
        ('devops', 'DevOps'),
        ('tools', 'Tools'),
        ('database', 'Database'),
    ]
    
    name = models.CharField(max_length=100, verbose_name="Nome Skill")
    category = models.CharField(
        max_length=20, 
        choices=CATEGORY_CHOICES, 
        default='backend',
        verbose_name="Categoria"
    )
    proficiency = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Livello",
        help_text="Da 1 a 5 stelle"
    )
    icon = models.CharField(
        max_length=50, 
        default='fas fa-code',
        verbose_name="Icona FontAwesome",
        help_text="Es. fas fa-python, fab fa-js"
    )
    order = models.IntegerField(default=0, verbose_name="Ordine")
    
    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ['category', 'order', 'name']
    
    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"


class Experience(models.Model):
    """
    Modello per le esperienze lavorative.
    """
    title = models.CharField(max_length=200, verbose_name="Titolo Posizione")
    company = models.CharField(max_length=200, verbose_name="Azienda")
    location = models.CharField(max_length=100, verbose_name="Luogo")
    description = models.TextField(verbose_name="Descrizione")
    start_date = models.DateField(verbose_name="Data Inizio")
    end_date = models.DateField(
        null=True, 
        blank=True, 
        verbose_name="Data Fine"
    )
    is_current = models.BooleanField(
        default=False, 
        verbose_name="Posizione Attuale"
    )
    order = models.IntegerField(default=0, verbose_name="Ordine")
    
    class Meta:
        verbose_name = "Esperienza"
        verbose_name_plural = "Esperienze"
        ordering = ['order', '-start_date']
    
    def __str__(self):
        return f"{self.title} @ {self.company}"


class ContactMessage(models.Model):
    """
    Modello per i messaggi di contatto ricevuti.
    """
    name = models.CharField(max_length=100, verbose_name="Nome")
    email = models.EmailField(verbose_name="Email")
    subject = models.CharField(max_length=200, verbose_name="Oggetto")
    message = models.TextField(verbose_name="Messaggio")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data")
    is_read = models.BooleanField(default=False, verbose_name="Letto")
    
    class Meta:
        verbose_name = "Messaggio"
        verbose_name_plural = "Messaggi"
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.subject} - {self.name}"


class SiteSettings(models.Model):
    """
    Impostazioni globali del sito. Dovrebbe esistere una sola istanza.
    """
    site_title = models.CharField(
        max_length=200, 
        default='Portfolio',
        verbose_name="Titolo Sito"
    )
    site_description = models.TextField(
        default='Portfolio di un Web & Mobile Developer',
        verbose_name="Descrizione Sito"
    )
    author_name = models.CharField(
        max_length=100, 
        default='Developer',
        verbose_name="Nome Autore"
    )
    author_bio = models.TextField(
        blank=True,
        verbose_name="Bio Autore"
    )
    author_image = models.ImageField(
        upload_to='profile/',
        blank=True,
        null=True,
        verbose_name="Foto Profilo"
    )
    email = models.EmailField(
        blank=True,
        verbose_name="Email"
    )
    phone = models.CharField(
        max_length=20, 
        blank=True,
        verbose_name="Telefono"
    )
    location = models.CharField(
        max_length=100, 
        blank=True,
        verbose_name="Località"
    )
    social_links = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Link Social",
        help_text='Es. {"github": "https://github.com/...", "linkedin": "..."}'
    )
    current_palette = models.ForeignKey(
        ColorPalette, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name="Palette Attiva"
    )
    
    class Meta:
        verbose_name = "Impostazioni Sito"
        verbose_name_plural = "Impostazioni Sito"
    
    def __str__(self):
        return self.site_title
    
    def save(self, *args, **kwargs):
        # Assicura che esista una sola istanza
        self.pk = 1
        super().save(*args, **kwargs)
    
    @classmethod
    def get_settings(cls):
        """Ottiene o crea le impostazioni del sito."""
        obj, created = cls.objects.get_or_create(pk=1)
        return obj
