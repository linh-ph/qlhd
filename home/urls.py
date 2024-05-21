from django.urls import path
from .views import Home, register, Index
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', Home.as_view(), name="home"),
    path('page/', Index.as_view(), name="index"),
    path('register/', register, name="register"),
    path('login/', auth_views.LoginView.as_view(template_name="pages/login.html"), name="login"),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]
