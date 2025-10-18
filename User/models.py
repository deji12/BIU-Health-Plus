from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, 
    PermissionsMixin
)
from cloudinary.models import CloudinaryField
from django.utils import timezone

class UserType:
    STUDENT = 'STUDENT'
    DOCTOR = 'DOCTOR'
    NURSE = 'NURSE'
    PHARMACIST = 'PHARMACIST'

USER_TYPE_CHOICES = [
    (UserType.DOCTOR, UserType.DOCTOR),
    (UserType.NURSE, UserType.NURSE),
    (UserType.STUDENT, UserType.STUDENT)
]

class CustomUserManager(BaseUserManager):
    def create_user(self, matric_number, password=None, **extra_fields):
        if not matric_number:
            raise ValueError('The matric_number field must be set')
        user = self.model(matric_number=matric_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(matric_number, password, **extra_fields)

class User(AbstractBaseUser, PermissionsMixin):
    matric_number = models.CharField(max_length=25, unique=True, help_text="The matric number of student")
    first_name = models.CharField(max_length=30, help_text="The user's first name.")
    middle_name = models.CharField(max_length=30, default='', null=True, blank=True, help_text="The user's middle name.")
    last_name = models.CharField(max_length=30, help_text="The user's last name.")
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default=UserType.STUDENT)

    serial_number = models.IntegerField(default=0)
    year_of_admission = models.IntegerField(default=timezone.now().year)

    profile_image = CloudinaryField(null=True, blank=True, folder='health-plus/user_profile_images/', help_text="User's profile image")

    staff_id = models.CharField(max_length=20, null=True, blank=True, help_text="Id of staff")
    verified_staff = models.BooleanField(default=False, help_text="Whether the staff is verified or not")

    is_staff =  models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False, help_text="Indicates whether the user has all admin permissions. Defaults to False.")
    is_active = models.BooleanField(default=True, help_text="Indicates whether the user account is active. Defaults to False and user needs to verify email on signup before it can be set to True.")
    date_joined = models.DateTimeField(auto_now_add=True, help_text="The date and time when the user joined.")
    
    objects = CustomUserManager()

    USERNAME_FIELD = 'matric_number'

    def get_full_name(self):
        return f"{self.first_name} {self.middle_name} {self.last_name}"