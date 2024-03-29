from .models import SellerProfile, SellerReview
from rest_framework import serializers
from .serializers import (ObtainAuthTokenSerializer,
                          CustomUserSerializer,
                          SellerReviewSerializer,
                          SellerProfileSerializer, CreateSellerProfileSerializer
                          )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status, views
from django.contrib.auth import get_user_model


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = ObtainAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
            }, status=status.HTTP_200_OK)


class RegisterUserView(generics.CreateAPIView):
    # Registering new users
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']

        # Checking if the username already exists
        if get_user_model().objects.filter(username=username).exists():
            return Response({'error': 'A user with that username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        user = serializer.save(is_staff=True)
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key,
                         'user_id': user.pk,
                         'username': user.username}, status=status.HTTP_201_CREATED)


class SellerProfileDetailView(generics.RetrieveAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = SellerProfileSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]


class SellerReviewCreateView(generics.CreateAPIView):
    queryset = SellerReview.objects.all()
    serializer_class = SellerReviewSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        seller_profile = generics.get_object_or_404(SellerProfile, user=self.request.user)
        serializer.save(reviewer=self.request.user, seller=seller_profile)
        seller_profile.total_reviews += 1
        seller_profile.total_ratings += serializer.validated_data['rating']
        seller_profile.average_rating = seller_profile.total_ratings / seller_profile.total_reviews
        seller_profile.save()


class CreateSellerProfileView(generics.CreateAPIView):
    queryset = SellerProfile.objects.all()
    serializer_class = CreateSellerProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # Checking if the user already has a seller profile
        user_profile = SellerProfile.objects.filter(user=self.request.user).first()

        if user_profile:
            # returning the needed message or error, If profile already exists
            return Response({"detail": "Seller profile already exists for this user."}, status=status.HTTP_400_BAD_REQUEST)

        # creating a new one, If the profile doesn't exist
        serializer.save(user=self.request.user)