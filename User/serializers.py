from rest_framework import serializers
from .models import User

class StudentSerializer(serializers.ModelSerializer):

    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = [
            'matric_number', 'first_name', 'last_name', 'middle_name',
            'user_type', 'serial_number', 'year_of_admission', 'profile_image',
            'date_joined'
        ]

    def get_profile_image(self, obj):
        return obj.user_profile_image()