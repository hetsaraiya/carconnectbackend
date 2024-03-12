from dj_rest_auth.serializers import LoginSerializer

from dj_rest_auth.registration.serializers import RegisterSerializer
from jsonschema import ValidationError
from rest_framework import serializers
from phonenumber_field.serializerfields import PhoneNumberField



def validate_username(value):
    invalid_characters = ["_", ".", ",", "&", "-", " ", "@", "#", "$", "%", "^"]
    for char in invalid_characters:
        if char in value:
            raise ValidationError(f"Username cannot include '{char}'.")

class NewRegisterSerializer(RegisterSerializer):
    MALE = 'M'
    FEMALE = 'F'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    username = serializers.CharField()
    name = serializers.CharField()
    contact_number = PhoneNumberField()
    email = serializers.EmailField()
    gender = serializers.ChoiceField(choices=GENDER_CHOICES)
    presenet_loc_longitude = serializers.FloatField()
    presenet_loc_latitude = serializers.FloatField()
    def custom_signup(self, request ,user):
        print("Custom signup method called")
        user.username = request.data["username"]
        user.name = request.data["name"]
        user.contact_number = request.data["contact_number"]
        user.email = request.data["email"]
        user.gender = request.data["gender"]
        user.presenet_loc_longitude = request.data["presenet_loc_longitude"]
        user.presenet_loc_latitude = request.data["presenet_loc_latitude"]
        user.save()



class NewLoginSerializer(LoginSerializer):
    pass