from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser

class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_pic')