from rest_framework import serializers
from api.models import CustomUser


class CustomUserSerializers(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['id', 'f_name', 'l_name', 'email', 'password', 'avatar', 'gender']
