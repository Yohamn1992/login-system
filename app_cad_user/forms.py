# app_cad_user/forms.py
from django import forms
from .models import Usuario  # Use o modelo personalizado

class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Usuario
        fields = ['username', 'email', 'password']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()
        return user

class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=254)
    senha = forms.CharField(label='Senha', widget=forms.PasswordInput)
