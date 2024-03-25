
from rest_framework import serializers
from .models import Company, Order, Paint, UserProfile
from django.contrib.auth.models import User
class PaintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paint
        fields = ['id', 'name', 'quantity']
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ['id', 'name', 'address']

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

class UserProfileSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    user = UserSerializer()
    class Meta:
        model = UserProfile
        fields = ['id', 'user', 'company', 'role']
        extra_kwargs = {'password': {'write_only': True},'email': {'write_only': True}}
    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['user']['username'], email=validated_data['user']['email'], password=validated_data['user']['password'])
        company = Company.objects.create(name=validated_data['company']['name'], address=validated_data['company']['address'])
        userprofile = UserProfile.objects.create(user=user, company=company, role=validated_data['role'])
        return userprofile
    
class OrderSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(slug_field='username', read_only=True)
    paint = serializers.SlugRelatedField(slug_field='name', read_only=True)
    company = serializers.SlugRelatedField(slug_field='name', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'paint', 'quantity', 'company']
    