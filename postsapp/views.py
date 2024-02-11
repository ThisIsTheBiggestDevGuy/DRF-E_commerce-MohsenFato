
from .models import Post, Category, Attribute, Chat
from postsapp.serializers import PostSerializer, CategorySerializer, ChatSerializer
from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from django.core.exceptions import PermissionDenied
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated, IsAuthenticatedOrReadOnly, AllowAny
from .permissions import IsOwnerOrReadOnly
from django.db.models import Q


class CategoryListCreateView(generics.ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]


class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        queryset = Post.objects.all()

        # Searching functionality:
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        # Filtering based on categories or other criteria
        category_id = self.request.query_params.get('category_id', None)

        if category_id:
            # fetching attributes
            category_attributes = self.get_category_attributes(category_id)
            # Looping through the category attributes and applying filters
            for attribute in category_attributes:
                attribute_name = attribute.name
                attribute_value = self.request.query_params.get(attribute_name, None)
                if attribute_value:
                    queryset = queryset.filter(attribute_values__attribute__name=attribute_name,
                                               attribute_values__value=attribute_value)

        return queryset

    def get_category_attributes(self, category_id):
        category = get_object_or_404(Category, pk=category_id)
        attributes = Attribute.objects.filter(category=category)
        return attributes

    def perform_create(self, serializer):
        # Setting the user field during post creation
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
            # Checking the phone number public Visibility
            hide_phone_number = self.request.data.get('hide_phone_number', False)
            if hide_phone_number:
                serializer.validated_data['phone_number'] = None
            serializer.save(user=self.request.user)

            # Fetching and including category attributes in the response
            category_id = self.request.data.get('category', None)
            if category_id:
                category_attributes = self.get_category_attributes(category_id)
                serializer.context['category_attributes'] = category_attributes

        else:
            raise PermissionDenied("Not allowed")


class PostRetrieveUpdateDeleteView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]


class ChatListCreateView(generics.ListCreateAPIView):
    queryset = Chat.objects.all()
    serializer_class = ChatSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(sender=self.request.user)

    def list(self, request, *args, **kwargs):
        # including chats in the response
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        chats_serializer = ChatSerializer(Chat.objects.all(), many=True)
        return Response({'posts': serializer.data, 'chats': chats_serializer.data})
