from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('login/', views.MyLoginView.as_view(), name='login'),
    path('signup/', views.MySignUpView.as_view(), name='signup'),
    path('show_myusers/', views.MyUserListView.as_view(), name='myuser-list'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', views.MyProfileView.as_view(), name='profile'),
]
