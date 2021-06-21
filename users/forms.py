from django.contrib.auth.forms import UserCreationForm
from .models import User

class NewUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('first_name','last_name','email','organization',)