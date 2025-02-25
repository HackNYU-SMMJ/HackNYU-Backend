from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.LoginView.as_view(), name='login'),
    path('callback/', views.CallbackView.as_view(), name='callback'),
    path("logout/", views.LogoutView.as_view(), name="logout"),
    path("", views.IndexView.as_view(), name="index"),
]