
from django.contrib.auth import get_user_model, authenticate, hashers
from rest_framework import serializers
from .models import CustomUser, SellerProfile, SellerReview


class ObtainAuthTokenSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)

            if user and user.is_active:
                data['user'] = user
            else:
                raise serializers.ValidationError('Unable to log in with the provided credentials.')
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ('id', 'username', 'password', 'email', 'is_seller')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        validated_data['password'] = hashers.make_password(validated_data.get('password'))
        return super().create(validated_data)


class SellerReviewSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReview
        fields = ['rating', 'comment']
        read_only_fields = ['seller', 'reviewer']


class SellerProfileSerializer(serializers.ModelSerializer):
    reviews = SellerReviewSerializer(many=True, read_only=True)

    class Meta:
        model = SellerProfile
        fields = '__all__'


class CreateSellerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerProfile
        fields = ['contact_info', 'bio']
