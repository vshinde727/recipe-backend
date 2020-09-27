from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import ugettext_lazy as _ 
from rest_framework import serializers

class UserSerializer(serializers.ModelSerializer):
    """Serializer for User model"""
    class Meta:
        model = get_user_model()
        fields = ('name','email','password')
        extra_kwargs = {'password': {"write_only": True, "min_length": 5}}

    def create(self, validated_data):
        """Create a new user with encrypted password and return it"""
        return get_user_model().objects.create_user(**validated_data)

class AuthTokenSerializer(serializers.Serializer):
    """Serializer for Authenctication token"""
    email = serializers.CharField()
    password = serializers.CharField(
        style = {'input_type':'password'},
        trim_whitespace = False 
    )

    def validate(self, attrs):
        """validate and authenticate user"""
        email = attrs.get('email')
        password = attrs.get('password')
        user = authenticate(
            request = self.context.get('request'),
            username = email,
            password = password
        )
        if not user:
            msg = _('Unable to authenticate with provided creds')
            raise serializers.ValidationError(msg, code='authentication')
        
        attrs['user'] = user
        return attrs