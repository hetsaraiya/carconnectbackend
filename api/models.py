from django.db import models
from django.core.validators import RegexValidator
from phonenumber_field.modelfields import PhoneNumberField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import AbstractUser, Group, Permission
# Create your models here.

no_special_chars_validator = RegexValidator(
    regex=r'^[^\s@#$%]+$',
    message='Special characters like @, #, $, % are not allowed.'
)

def validate_username(value):
    invalid_characters = ["_", ".", ",", "&", "-", " ", "@", "#", "$", "%", "^"]
    for char in invalid_characters:
        if char in value:
            raise ValidationError(f"Username cannot include '{char}'.")

class User(AbstractUser):

    groups = models.ManyToManyField(
        Group,
        verbose_name= ('groups'),
        blank=True,
        help_text= ('The groups this user belongs to. A user will get all permissions granted to each of their groups.'),
        related_name='custom_user_groups'  # Provide a unique related_name
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name= ('user permissions'),
        blank=True,
        help_text= ('Specific permissions for this user.'),
        related_name='custom_user_permissions'  # Provide a unique related_name
    )
    MALE = 'Male'
    FEMALE = 'Female'
    GENDER_CHOICES = [
        (MALE, 'Male'),
        (FEMALE, 'Female')
    ]
    uid = models.BigAutoField(primary_key=True)
    username = models.CharField(max_length=20, unique=True, validators=[validate_username])
    name = models.CharField(max_length=25)
    contact_number = PhoneNumberField(null=False, blank=False)
    email = models.EmailField(null=False, blank=False, unique=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES)
    presenet_loc_longitude = models.FloatField(blank=False, null=False, default=0.0)
    presenet_loc_latitude = models.FloatField(blank=False, null=False, default=0.0)
    
    def __str__(self):
        return self.username
    
    
class ServiceRequest(models.Model):
    requestId = models.BigAutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE, default=None)
    presenet_loc_longitude = models.FloatField(blank=False, null=False)
    presenet_loc_latitude = models.FloatField(blank=False, null=False)
    destination_loc_longitude = models.FloatField(blank=False, null=False)
    destination_loc_latitude = models.FloatField(blank=False, null=False)
    rider = models.OneToOneField(User, related_name="rider", on_delete=models.CASCADE, null=True)
    isDeleted = models.BooleanField(default=False)

    def __str__(self):
        return f"Request {self.requestId} from {self.user.username}"