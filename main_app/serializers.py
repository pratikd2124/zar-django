from rest_framework import serializers
from .models import User, ProfileInfo, Category

class ProfileInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfileInfo
        fields = [
            'brand_name', 'contact_number', 'contact_person', 'designation', 
            'bio', 'category',  
            'social_links', 'visible'
        ]

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'image', 'parent', 'description']

class UserSerializer(serializers.ModelSerializer):
    profile_info = ProfileInfoSerializer(many=True, read_only=True)
    category = CategorySerializer(many=True, read_only=True)

    class Meta:
        model = User
        fields = [
            'username', 'email', 'mobile', 
            'firm_name', 'address', 'country', 'state', 'city', 'zip_code',
            'contact_person', 'designation', 'bio', 'category', 'profile_info',
            'social_links', 'profile',
        ]
