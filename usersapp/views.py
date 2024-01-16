from .models import SellerProfile, SellerReview
from .serializers import (ObtainAuthTokenSerializer,
                          CustomUserSerializer,
                          SellerReviewSerializer,
                          SellerProfileSerializer
                          )
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import generics, permissions, status, views
from django.contrib.auth import get_user_model
# Create your views here.


class LoginView(views.APIView):
    def post(self, request, *args, **kwargs):
        serializer = ObtainAuthTokenSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data('user')
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username
            }, status=status.HTTP_200_OK)


class RegisterUserView(generics.CreateAPIView):
    # Register new users
    queryset = get_user_model().objects.all()
    serializer_class = CustomUserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        username = serializer.validated_data['username']

        # Check if the username already exists
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

