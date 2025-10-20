from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)
from cloudinary.models import CloudinaryField
from django.utils import timezone
from rest_framework_simplejwt.tokens import RefreshToken
from django.conf import settings


class UserType:
    STUDENT = 'student'
    DOCTOR = 'doctor'
    NURSE = 'nurse'
    PHARMACIST = 'pharmacist'
    ADMIN = 'admin'

    @classmethod
    def list(cls):
        return [value for key, value in cls.__dict__.items() if key.isupper()]


USER_TYPE_CHOICES = [
    (UserType.DOCTOR, UserType.DOCTOR),
    (UserType.NURSE, UserType.NURSE),
    (UserType.STUDENT, UserType.STUDENT),
    (UserType.ADMIN, UserType.ADMIN),
]


class CustomUserManager(BaseUserManager):
    def create_user(self, matric_number=None, password=None, **extra_fields):
        user = self.model(matric_number=matric_number, **extra_fields)
        if password:
            user.set_password(password)
        else:
            user.set_unusable_password()
        user.save(using=self._db)
        return user

    def create_superuser(self, matric_number=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(matric_number, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    matric_number = models.CharField(
        max_length=25,
        null=True,
        blank=True,
        unique=True,
        help_text="The matric number of the student (optional)."
    )
    first_name = models.CharField(max_length=30, help_text="The user's first name.")
    middle_name = models.CharField(
        max_length=30,
        default='',
        null=True,
        blank=True,
        help_text="The user's middle name."
    )
    last_name = models.CharField(max_length=30, help_text="The user's last name.")
    user_type = models.CharField(
        max_length=15,
        choices=USER_TYPE_CHOICES,
        default=UserType.STUDENT
    )

    serial_number = models.IntegerField(default=0)
    year_of_admission = models.IntegerField(default=timezone.now().year)

    profile_image = CloudinaryField(
        null=True,
        blank=True,
        folder='health-plus/user_profile_images/',
        help_text="User's profile image."
    )

    staff_id = models.CharField(
        max_length=20,
        unique=True,
        null=True,
        blank=True,
        help_text="The ID of the staff member."
    )
    staff_id_img = CloudinaryField(
        null=True,
        blank=True,
        folder='health-plus/staff_id_img',
        help_text="The image of the staff ID card."
    )
    verified_staff = models.BooleanField(
        default=False,
        help_text="Whether the staff is verified or not."
    )

    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(
        default=False,
        help_text="Indicates whether the user has all admin permissions."
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Indicates whether the user account is active."
    )
    date_joined = models.DateTimeField(auto_now_add=True, help_text="Date user joined.")

    objects = CustomUserManager()

    USERNAME_FIELD = 'matric_number'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def get_full_name(self):
        names = [self.first_name]
        if self.middle_name:
            names.append(self.middle_name)
        names.append(self.last_name)
        return " ".join(names).strip()

    def auth_tokens(self):
        refresh = RefreshToken.for_user(self)
        self.last_login = timezone.now()
        self.save()
        return {
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        }

    def user_profile_image(self):
        if self.profile_image:
            return self.profile_image.url
        return settings.DEFAULT_USER_PROFILE_IMAGE

    def __str__(self):
        return self.get_full_name()