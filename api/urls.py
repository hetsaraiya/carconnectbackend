from .views import signUp, signIn
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("signup/", signUp, name="signup"),
    path("signin/", signIn, name="signin"),
]