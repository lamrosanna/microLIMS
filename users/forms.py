from django.contrib.auth.forms import UserChangeForm, UserCreationForm

from .models import LIMSuser

class LIMSuserForm(UserCreationForm):
    class Meta:
        model = LIMSuser
        fields=("email", "first_name", "last_name","company")

class LIMSuserChangeForm(UserChangeForm):
    class Meta:
        model = LIMSuser
        fields=("email", "first_name", "last_name","company")
