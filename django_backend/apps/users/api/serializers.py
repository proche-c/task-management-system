from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from rest_framework import serializers

# Gets the user by default set on settings.py
User = get_user_model()

class   UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model.

    Converts User model instances into JSON representations and validates input
    for updating or retreiving user information.

    Fields:
        id (int): Primary key of the user.
        username (str): Username of the user.
        email (str): Email address of the user.
        team (Team): Associated team of the user (nullable).
    """
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'team']


class RegisterSerializer(serializers.ModelSerializer):
    """
    Serializer for registering new users.

    Handles user creation with password validation and password confirmation.

    Fields:
        id (int): Primary key of the new user.
        username (str): Username of the new user.
        email (str): Email address of the new user.
        password (str): Password for the new user (write-only).
        password2 (str): Password confirmation (write-only).    

    Methods:
        validate: Ensures that password and password2 math and validates password strength.
        create: Creates and saves a new User instance with hashed password. 
    """
    password = serializers.CharField(write_only=True)
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "email", "password", "password2"]

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Passwords do not match")
        validate_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop("password2")
        user = User(**validated_data)
        user.set_password(validated_data["password"])
        user.save()
        return user

