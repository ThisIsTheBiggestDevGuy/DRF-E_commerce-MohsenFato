from .serializers import ObtainAuthTokenSerializer, CustomUserSerializer
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

