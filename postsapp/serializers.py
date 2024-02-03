
from .models import Post, Category, Chat, Attribute
from rest_framework import serializers


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chat
        fields = '__all__'


class PostSerializer(serializers.ModelSerializer):
    chats = ChatSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = "__all__"


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = '__all__'


class CategorySerializer(serializers.ModelSerializer):
    attributes = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = '__all__'

    def get_attributes(self, category):
        attributes = Attribute.objects.filter(category=category)
        return AttributeSerializer(attributes, many=True).data
