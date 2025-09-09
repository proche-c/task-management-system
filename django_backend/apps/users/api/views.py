from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import viewsets, status
from rest_framework.decorators import action, permission_classes
from rest_framework.response import Response
from .serializers import RegisterSerializer, UserSerializer
from .pagination import UsersPagination

User = get_user_model()

class AuthViewSet(viewsets.ViewSet):
    """
    ViewSet for handling user authentication.

    Provides endpoints for:
    - register: Register a new user.
        Expects:username, email, password,  password2
        Returns:
            - 201 with user data if successful
            - 400 with validation errors if invalid
    - login: Authenticate a user and return JWT tokens.
        Expects:username, password
        Returns:
            - 200 with access and refresh tokens if credentials are valid
            - 401 if credentials are invalid    
    - logout: Log out the current user.
        Returns:
            - 200 with success message
    - refresh: Refresh an access token using a valid refresh token.
        Expects: refresh (the refresh token string)
        Returns:
            - 200 with new access token if refresh is valid
            - 400 if refresh token is missing or invalid
    """
    permission_classes = []

    @action(detail=False, methods=["post"], permission_classes=[AllowAny])
    def register(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(UserSerializer(user).data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["post"])
    def login(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        user = authenticate(request, username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                "access": str(refresh.access_token),
                "refresh": str(refresh),
            })
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

    @action(detail=False, methods=["post"])
    def logout(self, request):
        logout(request)
        return Response({"message": "Logged out successfully"})

    @action(detail=False, methods=["post"])
    def refresh(self, request):
        refresh_token = request.data.get("refresh")
        if not refresh_token:
            return Response({"error": "Refresh token required"}, status=status.HTTP_400_BAD_REQUEST)
        try:
            refresh = RefreshToken(refresh_token)
            access_token = refresh.access_token
            return Response({"access": str(access_token)})
        except Exception as e:
            return Response({"error": "Invalid refresh token"}, status=status.HTTP_400_BAD_REQUEST)
    
class UserViewSet(viewsets.ViewSet):
    """
    ViewSet for managing users.

    Requires authentication for all endpoints.  
    Provides endpoints for:
    - list: Listing users with pagination
        Returns: a paginated list of users with their team info.
    - retrieve: Retrieving a single user by ID
        Retrieve details of a specific user by ID.
        Returns: user data if found, otherwise 404.
    - update: Updating a user
        Expects: full user data (not partial).  
        Returns: updated user data or validation errors.
    - me: Retrieving the currently authenticated user
        Retrieve details of the currently authenticated user.
        Returns: user data with team info.
    """

    permission_classes = [IsAuthenticated]
    pagination_class = UsersPagination

    def list(self, request):
        users = User.objects.select_related('team').all()
        paginator = UsersPagination()
        result_page = paginator.paginate_queryset(users, request)
        serializer = UserSerializer(result_page, many=True)
        return paginator.get_paginated_response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            user = User.objects.select_related('team').get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def update(self, request, pk=None):
        try:
            user = User.objects.get(pk=pk)
        except User.DoesNotExist:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)
        serializer = UserSerializer(user, data=request.data, partial=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(detail=False, methods=["get"])
    def me(self, request):
        user = User.objects.select_related('team').get(pk=request.user.pk)
        serializer = UserSerializer(user)
        return Response(serializer.data)