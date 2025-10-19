from django.urls import path
from .views import (
    register_student, login_user
)

BASE_URL = 'auth'

urlpatterns = [
    path(f'{BASE_URL}/register/student/', register_student, name='register_student'),
    path(f'{BASE_URL}/login/', login_user, name='login_user'),
]