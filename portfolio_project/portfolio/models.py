from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator


class Project(models.Model):
    """
    Modello per i progetti del portfolio.
    """

    CATEGORY_CHOICES = [
        ("web", "Web Development"),
        ("mobile", "Mobile Development"),
        ("fullstack", "Full Stack"),
    ]

    title = models.CharField(max_length=200, verbose_name="Titolo")
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    description = models.TextField(verbose_name="Descrizione Completa")
    short_description = models.CharField(
        max_length=300, verbose_name="Descrizione Breve"
    )
    image = models.ImageField(
        upload_to="projects/", verbose_name="Immagine Principale", blank=True, null=True
    )
    technologies = models.CharField(
        max_length=500,
        verbose_name="Tecnologie",
        help_text="Separare con virgola (es. Python, Django, React)",
    )
    project_url = models.URLField(blank=True, null=True, verbose_name="URL Progetto")
    github_url = models.URLField(blank=True, null=True, verbose_name="URL GitHub")
    category = models.CharField(
        max_length=20, choices=CATEGORY_CHOICES, default="web", verbose_name="Categoria"
    )
    featured = models.BooleanField(default=False, verbose_name="In Evidenza")
    order = models.IntegerField(default=0, verbose_name="Ordine")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Progetto"
        verbose_name_plural = "Progetti"
        ordering = ["order", "-created_at"]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def get_technologies_list(self):
        return [tech.strip() for tech in self.technologies.split(",")]


class Skill(models.Model):
    """
    Modello per le competenze tecniche.
    """

    CATEGORY_CHOICES = [
        ("backend", "Backend"),
        ("frontend", "Frontend"),
        ("mobile", "Mobile"),
        ("devops", "DevOps"),
        ("tools", "Tools"),
        ("database", "Database"),
    ]

    name = models.CharField(max_length=100, verbose_name="Nome Skill")
    category = models.CharField(
        max_length=20,
        choices=CATEGORY_CHOICES,
        default="backend",
        verbose_name="Categoria",
    )
    proficiency = models.IntegerField(
        default=3,
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        verbose_name="Livello",
        help_text="Da 1 a 5 stelle",
    )
    icon = models.CharField(
        max_length=50,
        default="fas fa-code",
        verbose_name="Icona FontAwesome",
        help_text="Es. fas fa-python, fab fa-js",
    )
    order = models.IntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Skill"
        verbose_name_plural = "Skills"
        ordering = ["category", "order", "name"]

    def __str__(self):
        return f"{self.name} ({self.get_category_display()})"

    @property
    def level(self):
        return self.proficiency * 20


class Experience(models.Model):
    """
    Modello per le esperienze lavorative.
    """

    title = models.CharField(max_length=200, verbose_name="Titolo Posizione")
    company = models.CharField(max_length=200, verbose_name="Azienda")
    location = models.CharField(max_length=100, verbose_name="Luogo")
    description = models.TextField(verbose_name="Descrizione")
    start_date = models.DateField(verbose_name="Data Inizio")
    end_date = models.DateField(null=True, blank=True, verbose_name="Data Fine")
    is_current = models.BooleanField(default=False, verbose_name="Posizione Attuale")
    order = models.IntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Esperienza"
        verbose_name_plural = "Esperienze"
        ordering = ["order", "-start_date"]

    def __str__(self):
        return f"{self.title} @ {self.company}"


class Education(models.Model):
    """
    Modello per il percorso di studi e formazione.
    """

    title = models.CharField(max_length=200, verbose_name="Titolo Corso/Diploma")
    institution = models.CharField(max_length=200, verbose_name="Istituto/Scuola")
    hours = models.IntegerField(
        null=True, blank=True, verbose_name="Ore Totali", help_text="Esempio: 100"
    )
    description = models.TextField(verbose_name="Descrizione", blank=True)
    order = models.IntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Formazione"
        verbose_name_plural = "Formazione"
        ordering = ["order", "title"]

    def __str__(self):
        return f"{self.title} @ {self.institution}"


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
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.subject} - {self.name}"


class SiteSettings(models.Model):
    """
    Impostazioni globali del sito. Dovrebbe esistere una sola istanza.
    """

    site_title = models.CharField(
        max_length=200, default="Portfolio", verbose_name="Titolo Sito"
    )
    site_description = models.TextField(
        default="Portfolio di un Web & Mobile Developer",
        verbose_name="Descrizione Sito",
    )
    author_name = models.CharField(
        max_length=100, default="Developer", verbose_name="Nome Autore"
    )
    author_bio = models.TextField(blank=True, verbose_name="Bio Autore")
    author_image = models.ImageField(
        upload_to="profile/", blank=True, null=True, verbose_name="Foto Profilo (About)"
    )
    homepage_image = models.ImageField(
        upload_to="profile/", blank=True, null=True, verbose_name="Foto Homepage"
    )
    cv_file = models.FileField(
        upload_to="cv/", blank=True, null=True, verbose_name="File CV (PDF)"
    )
    email = models.EmailField(blank=True, verbose_name="Email")
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefono")
    location = models.CharField(max_length=100, blank=True, verbose_name="Località")
    social_links = models.JSONField(
        default=dict,
        blank=True,
        verbose_name="Link Social",
        help_text='Es. {"github": "https://github.com/...", "linkedin": "..."}',
    )

    class Meta:
        verbose_name = "Impostazioni Sito"
        verbose_name_plural = "Impostazioni Sito"

    def __str__(self):
        return self.site_title

    def save(self, *args, **kwargs):
        self.pk = 1
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, created = cls.objects.get_or_create(pk=1)
        return obj


class Certification(models.Model):
    """
    Modello per le certificazioni ottenute.
    """

    title = models.CharField(max_length=200, verbose_name="Titolo Certificazione")
    issuing_organization = models.CharField(
        max_length=200, verbose_name="Ente Emittente"
    )
    issue_date = models.DateField(verbose_name="Data di Rilascio")
    certificate_image = models.ImageField(
        upload_to="certifications/",
        verbose_name="Immagine Certificato",
        blank=True,
        null=True,
    )
    verification_url = models.URLField(
        blank=True, null=True, verbose_name="URL di Verifica"
    )
    description = models.TextField(blank=True, verbose_name="Descrizione")
    order = models.IntegerField(default=0, verbose_name="Ordine")

    class Meta:
        verbose_name = "Certificazione"
        verbose_name_plural = "Certificazioni"
        ordering = ["-issue_date", "order"]

    def __str__(self):
        return f"{self.title} - {self.issuing_organization}"
