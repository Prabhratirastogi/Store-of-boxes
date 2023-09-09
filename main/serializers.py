from rest_framework import serializers
from .models import Box, User
from rest_framework.authtoken.models import Token

class BoxListSerializer(serializers.ModelSerializer):
    created_by = serializers.CharField(source='created_by_username', read_only = True)
    last_updated = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S.%fZ", read_only=True)

    class Meta:
        model = Box
        # fields = ['length', 'width', 'height','created_by', 'last_updated']
        fields = "__all__"
        
class BoxCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['length', 'width', 'height']

class BoxUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = ['length', 'width', 'height']

    def update(self,instance, validated_data):
        validated_data.pop('Created By', None)
        validated_data.pop('created_at', None)

        return super().update(instance, validated_data)
    

class TokenSerializer(serializers.ModelSerializer):
    class Meta:
        model = Token
        fields = ('user', 'key')

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'password')

class BoxDeleteSerializer(serializers.Serializer):
    box_id = serializers.IntegerField()