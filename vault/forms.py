from django.forms import ModelForm, PasswordInput

from vault.models import Credential


class CredentialForm(ModelForm):
    class Meta:
        model = Credential
        fields = '__all__'
        widgets = {
            'password': PasswordInput()
        }
