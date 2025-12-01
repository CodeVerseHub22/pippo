from django import forms
from .models import ContactMessage


class ContactForm(forms.ModelForm):
    """
    Form per il contatto.
    """
    class Meta:
        model = ContactMessage
        fields = ['name', 'email', 'subject', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Il tuo nome',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'La tua email',
                'required': True
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Oggetto del messaggio',
                'required': True
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Il tuo messaggio...',
                'rows': 6,
                'required': True
            }),
        }
        labels = {
            'name': 'Nome',
            'email': 'Email',
            'subject': 'Oggetto',
            'message': 'Messaggio',
        }
    
    def clean_email(self):
        """Validazione aggiuntiva per l'email."""
        email = self.cleaned_data.get('email')
        if email:
            email = email.lower().strip()
        return email
    
    def clean_message(self):
        """Validazione per il messaggio."""
        message = self.cleaned_data.get('message')
        if message and len(message) < 10:
            raise forms.ValidationError(
                "Il messaggio deve contenere almeno 10 caratteri."
            )
        return message
