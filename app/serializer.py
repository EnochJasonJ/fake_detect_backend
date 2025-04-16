from .models import GetUrlModel, StoreURLDetailsModel
from rest_framework import serializers
from urllib.parse import urlparse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate


class URLSerializers(serializers.ModelSerializer):
    class Meta:
        model = GetUrlModel
        fields = '__all__'
        read_only_fields = ['user']

    def validate_Product_URL(self,value):
        parsed_URL = urlparse(value)
        if not parsed_URL.scheme:
            value = "http://"+value
            parsed_URL = urlparse(value)
        if not parsed_URL.scheme or not parsed_URL.netloc:
            raise serializers.ValidationError('Enter a valid URL.')
        if '.' not in parsed_URL.netloc:
            raise serializers.ValidationError("Enter a valid domain in the URL.")
        return value
    
class ScrapeURLSerializer(serializers.ModelSerializer):
    class Meta:
        model = StoreURLDetailsModel
        fields = '__all__'



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
    def create(self,validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            email = validated_data["email"],
            password = validated_data["password"]
        )
        user.is_staff = True
        user.save()
        return user
    


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only = True)

    def validate(self,data):
        user = authenticate(username = data['username'],password = data['password'])
        if user and user.is_active:
            return {"user": user}
        raise serializers.ValidationError("Invalid credentials.")