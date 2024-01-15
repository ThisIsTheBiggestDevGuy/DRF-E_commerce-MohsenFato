
from .models import Post, Category, Attribute, Chat
from postsapp.serializers import PostSerializer, CategorySerializer, ChatSerializer
# Create your views here.
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

    def perform_create(self, serializer):
        # Set the user field during post creation
        if self.request.user.is_authenticated:
            serializer.save(user=self.request.user)
            # check if user wants to hide phone number
            hide_phone_number = self.request.data.get('hide_phone_number', False)
            if hide_phone_number:
                serializer.validated_data['phone_number'] = None
            serializer.save(user=self.request.user)
        else:
            raise PermissionDenied("Not allowed")

    def get_queryset(self):
        queryset = Post.objects.all()

        # searching functionality:
        search_query = self.request.query_params.get('search', None)
        if search_query:
            queryset = queryset.filter(
                Q(title__icontains=search_query) |
                Q(description__icontains=search_query)
            )
        # filtering based on categories or other criteria
        category_id = self.request.query_params.get('category_id', None)

        def get_category_attributes(category_id):
            try:
                category = Category.objects.get(pk=category_id)
                attributes = Attribute.objects.filter(category=category)
                return [attribute.name for attribute in attributes]
            except Category.DoesNotExist:
                # The case where the category doesn't exist
                return Response({'error': 'Category not found'}, status=status.HTTP_404_NOT_FOUND)
            except Attribute.DoesNotExist:
                # The case where there are no attributes for the category
                return Response({'message': 'No attributes found for the category'}, status=status.HTTP_200_OK)
        category_attributes = get_category_attributes(category_id)

        if category_id:
            category_attributes = get_category_attributes(category_id)
            # Loop through the category attributes and apply filters
            for attribute in category_attributes:
                attribute_name = attribute.name
                attribute_value = self.request.query_params.get(attribute_name, None)
                if attribute_value:
                    queryset = queryset.filter(attribute_values__attribute__name=attribute_name,
                                               attribute_values__value=attribute_value)

        return queryset


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
