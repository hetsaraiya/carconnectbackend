import json
from django.http import HttpResponse
from django.shortcuts import render
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User
from .models import *
# Create your views here.


@csrf_exempt
def signUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('fname')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        presenet_loc_longitude = request.POST.get('presenet_loc_longitude')
        presenet_loc_latitude = request.POST.get('presenet_loc_latitude')
        password = request.POST.get('password')
        confirmPassword = request.POST.get('Confirm Password')
        
        if User.objects.filter(username=username):
            messages.error(request, "Username already exist! Please try some other username.")
            return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
        
        if len(username)>20:
            messages.error(request, "Username must be under 20 charcters!!")
            
        
        if password != confirmPassword:
            messages.error(request, "Passwords didn't matched!!")
        

        myuser=User.objects.create_user(username, email, password)
        myuser.name = name
        myuser.email = email
        myuser.contact_number = "+91" + contact_number
        myuser.gender = gender
        myuser.presenet_loc_longitude = presenet_loc_longitude
        myuser.presenet_loc_latitude = presenet_loc_latitude
        # myuser.is_active = False
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check mail for confirmation")
        return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
    
@csrf_exempt
def signIn(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
        else:
            messages.error(request, "Bad Credentials!!")
            return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)
    
    return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)


@csrf_exempt
def signout(request):
    logout(request)
    messages.success(request, "Logged Out Successfully!!")
    return HttpResponse(json.dumps({"msg": " your details updated successfully."}),content_type="application/json",)

@csrf_exempt
def makeRequest(request):
    if request.method == "POST":

        servicerequest = ServiceRequest()
        user = request.POST.get("user")
        users = User.objects.get(username=user)
        presenet_loc_longitude = request.POST.get("presenet_loc_longitude")
        presenet_loc_latitude = request.POST.get("presenet_loc_latitude")
        destination_loc_longitude = request.POST.get("destination_loc_longitude")
        destination_loc_latitude = request.POST.get("destination_loc_latitude")
        isDeleted = request.POST.get("isDeleted")

        servicerequest.user = users
        servicerequest.presenet_loc_longitude = presenet_loc_longitude
        servicerequest.presenet_loc_latitude = presenet_loc_latitude
        servicerequest.destination_loc_longitude = destination_loc_longitude
        servicerequest.destination_loc_latitude = destination_loc_latitude
        servicerequest.isDeleted = isDeleted
        servicerequest.save()