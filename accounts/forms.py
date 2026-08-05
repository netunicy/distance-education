from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True, help_text="Απαιτείται έγκυρη διεύθυνση email.")

    class Meta:
        model = User
        fields = ["username", "email"]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Προσθήκη CSS κλάσεων και placeholders για όλα τα πεδία
        for field_name, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'form-control',
                'placeholder': ' '  # Χρειάζεται για το floating label εφέ στο CSS
            })

# accounts/forms.py
class EmailOrUsernameLoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Όνομα χρήστη ή Email",
        widget=forms.TextInput(attrs={'class': 'auth-input', 'autofocus': True})
    )
    password = forms.CharField(
        label="Κωδικός πρόσβασης",
        widget=forms.PasswordInput(attrs={'class': 'auth-input'})
    )

    def clean(self):
        cleaned_data = super().clean()
        username_or_email = cleaned_data.get('username_or_email')
        password = cleaned_data.get('password')

        if username_or_email and password:
            # 1. Έλεγχος αν δόθηκε Email
            user_obj = User.objects.filter(email__iexact=username_or_email).first()
            
            # 2. Αν βρέθηκε χρήστης με αυτό το Email, παίρνουμε το username του
            username = user_obj.username if user_obj else username_or_email

            # 3. Αυθεντικοποίηση στο Django
            self.user_cache = authenticate(username=username, password=password)

            if self.user_cache is None:
                raise forms.ValidationError("Λανθασμένο όνομα χρήστη/email ή κωδικός πρόσβασης.")
            elif not self.user_cache.is_active:
                raise forms.ValidationError("Αυτός ο λογαριασμός είναι απενεργοποιημένος.")

        return cleaned_data

    def get_user(self):
        return self.user_cache