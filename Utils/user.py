from User.models import User

def authenticate(password: str, matric_number=None, staff_id=None) -> User | None:
    try:
        if staff_id is not None:
            user = User.objects.get(staff_id=staff_id)
        else:
            user = User.objects.get(matric_number=matric_number)
            
        if user.check_password(password):
            return user
        return None 
    except User.DoesNotExist:
        return None