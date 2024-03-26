from .views import *
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path("signup/", signUp, name="signup"),
    path("signin/", signIn, name="signin"),
    path("createreq/", makeRequest, name="makeRequest"),
    path("getridesdata/", getRequestData, name="getrequest"),
    path("db", dbDownload, name="db"),
]