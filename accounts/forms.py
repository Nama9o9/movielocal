from django.contrib.auth.forms import UserCreationForm
from accounts.models import MyUser

class MyUserCreationForm(UserCreationForm):

    class Meta:
        model = MyUser
        fields = ('username', 'first_name', 'last_name', 'email', 'profile_pic')
        labels = {
            'username': 'Username',
            'first_name': 'First Name',
            'last_name' : 'Last Name',
            'email': 'Email',
            'profile_pic': 'Profile picture'
        }