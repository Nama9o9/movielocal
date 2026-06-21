from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponseRedirect

from .forms import MyUserCreationForm
from .models import MyUser
from django.urls import reverse_lazy
from django.views import generic
from django.contrib.auth import (
    login as auth_login,
)
from django.contrib.auth.views import LoginView


# Create your views here.
class MySignUpView(generic.CreateView):
    form_class = MyUserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'registration/signup.html'

class MyLoginView(LoginView):
    template_name = 'registration/login.html'


class MyUserListView(generic.ListView):
    model = MyUser
    context_object_name = 'all_myusers'
    template_name = 'myuser_list.html'

class MyProfileView(LoginRequiredMixin, generic.TemplateView):
    template_name = 'profile.html'




