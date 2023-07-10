from django.contrib.auth.forms import UserCreationForm
from .models import BuyForCryptoUser


class RegistrationForm(UserCreationForm):
    class Meta:
        model = BuyForCryptoUser
        fields = ['username', 'email']
