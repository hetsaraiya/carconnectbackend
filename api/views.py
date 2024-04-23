import json
import os
from django.http import HttpResponse
from django.shortcuts import render
import requests
import json
from django.http import JsonResponse
from rest_framework import generics
from django.core import serializers as serializer
from .serializers import *
from rest_framework.authtoken.models import Token
from django.contrib import messages
from geopy.geocoders import MapQuest
from django.contrib.auth import authenticate, login, logout
from django.views.decorators.csrf import csrf_exempt,csrf_protect
from django.contrib.auth.models import User
from .models import *
# Create your views here.

# https://www.mapquestapi.com/geocoding/v1/reverse?key=KEY&location=30.333472,-81.470448&includeRoadMetadata=true&includeNearestIntersection=true

# KEY = "Your_API_KEY"
KEY = "kBEVbZm3gsQjxw9AxkAwjUbICySUacls"

def get_address(latitude, longitude):
    try:
        response = requests.get(f"https://www.mapquestapi.com/geocoding/v1/reverse?key={KEY}&location={latitude},{longitude}&includeRoadMetadata=true&includeNearestIntersection=true")
        response.raise_for_status()  # Raise an error for non-2xx status codes
        
        # Check if response content is JSON
        try:
            location_data = response.json()
        except ValueError:
            print("Response content is not JSON:", response.content)
            return "Unknown"
        
        # Extract address components
        address = location_data.get("results", [])[0].get("locations", [])[0]
        street = address.get("street", "Unknown")
        city = address.get("adminArea5", "Unknown")
        state = address.get("adminArea3", "Unknown")
        country = address.get("adminArea1", "Unknown")

        # Construct the full address
        full_address = f"{street}, {city}, {state}, {country}"
        return full_address
    except requests.RequestException as e:
        # Handle request exceptions
        print(f"Error during reverse geocoding: {e}")
        return "Unknown"


@csrf_exempt
def signUp(request):
    if request.method == "POST":
        username = request.POST.get('username')
        name = request.POST.get('name')
        contact_number = request.POST.get('contact_number')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        presenet_loc_longitude = request.POST.get('presenet_loc_longitude')
        presenet_loc_latitude = request.POST.get('presenet_loc_latitude')
        password = request.POST.get('password1')
        confirmPassword = request.POST.get('password2')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exist! Please try some other username.")
            return HttpResponse(json.dumps({"msg": " UserName Already Exists."}),content_type="application/json",)
        
        if User.objects.filter(email=email).exists():
            messages.error(request, "Email Already Registered!!")
            return HttpResponse(json.dumps({"msg": " Email Already In Use."}),content_type="application/json",)
        
        if password != confirmPassword:
            return HttpResponse(json.dumps({"msg": "Password and ConfirmPassword Are Not Equal"}),content_type="application/json")
        
        
        

        myuser=User.objects.create_user(username=username, email=email, password=password)
        myuser.name = name
        myuser.email = email
        myuser.contact_number = "+91" + contact_number
        myuser.gender = gender
        myuser.presenet_loc_longitude = presenet_loc_longitude
        myuser.presenet_loc_latitude = presenet_loc_latitude
        myuser.is_active = True
        myuser.save()
        messages.success(request, "Your Account has been created succesfully!! Please check mail for confirmation")
        return HttpResponse(json.dumps({"msg": " Your Details Are Updated Successfully."}),content_type="application/json",)
    else:
        return HttpResponse(json.dumps({"msg": "Bad Request"}))
    
@csrf_exempt
def signIn(request):
    if request.method == "POST":
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponse(json.dumps({"msg": " Logged In "}),content_type="application/json",)
        else:
            messages.error(request, "Bad Credentials!!")
            return HttpResponse(json.dumps({"msg": " Invalid Credentials "}),content_type="application/json",)
    
    return HttpResponse(json.dumps({"msg": " Invalid Request "}),content_type="application/json",)


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
        presenet_loc_longitude = float(request.POST.get("presenet_loc_longitude"))
        presenet_loc_latitude = float(request.POST.get("presenet_loc_latitude"))
        destination = request.POST.get("destination_address")
        geolocator = MapQuest(api_key=KEY)
        destination_location = geolocator.geocode(destination)
        # isDeleted = request.POST.get("isDeleted")
        if ServiceRequest.objects.get(user=users.pk):
            return HttpResponse(json.dumps({"msg" : "Already Exists"}))

        servicerequest.user = users
        servicerequest.presenet_loc_longitude = presenet_loc_longitude
        servicerequest.presenet_loc_latitude = presenet_loc_latitude
        servicerequest.destination_loc_longitude = destination_location.longitude
        servicerequest.destination_loc_latitude = destination_location.latitude
        # servicerequest.isDeleted = 
        servicerequest.save()

        return HttpResponse(json.dumps({"msg": "Ride availed"}))
    
    else:
        return HttpResponse(json.dumps({"msg": "Bad Request"}))

@csrf_exempt
def getRequestData(request):
    if request.method == "GET":
        avilablerides = ServiceRequest.objects.filter(isDeleted=False).all()
        
        rides = []
        for ride in avilablerides:
            riderLocation = get_address(ride.presenet_loc_latitude, ride.presenet_loc_longitude)
            riderDestination = get_address(ride.destination_loc_latitude, ride.destination_loc_longitude)
            ride_data = {
                "username" : ride.user.name,
                "username": ride.user.username,
                "userlocation" : riderLocation,
                "userDestination" : riderDestination,
                "contact_number" : str(ride.user.contact_number),
            }
            rides.append(ride_data)
        return JsonResponse(rides, safe=False)
    else:
        return HttpResponse(json.dumps({"msg": "Bad Request"}))
    
@csrf_exempt
def dbDownload(request):
    if request.user.is_superuser:
        os.system("cp db.sqlite3 static/")
        return HttpResponse("<a href='/static/db.sqlite3' download>Download</a>")
    
@csrf_exempt
def getData(request):
    if request.method == "GET":
        id = request.GET.get("id")
        user = User.objects.get(pk=id)
        token = Token.objects.get(user=user.pk)
        response = {
            "pk":user.pk,
            "username": user.username,
            "email": user.email,
            "name": user.first_name + user.last_name,
            "token": token.key,
            "gender": user.gender,
            "contact_number" : str(user.contact_number)
        }
        return HttpResponse(json.dumps(response))
    else:
        return HttpResponse(json.dumps({"msg" : "Invalid token"}))

    
@csrf_exempt
def hookUser(request):
    if request.method == "POST":
        username = request.POST.get("username")
        rider_id = request.POST.get("rider")
        user = User.objects.get(username=username)
        rider = User.objects.get(pk=rider_id)
        req = ServiceRequest.objects.get(user=user.pk)
        req.rider = rider
        return HttpResponse(json.dumps({"msg" : "Success"}))
    else:
        return HttpResponse(json.dumps({"msg" : "Bad request"}))