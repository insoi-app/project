from django.shortcuts import render
from rest_framework.generics import GenericAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserRegistrationSerializer, UserLoginSerializer, CustomUserSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication

class UserRegistrationAPIView(GenericAPIView):
    permission_classes = [AllowAny]  # Ensure permission_classes is a list
    authentication_classes = []  # No authentication needed for registration
    serializer_class = UserRegistrationSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = RefreshToken.for_user(user)
        data = serializer.data
        data["tokens"] = {"refresh": str(token),
                          "access": str(token.access_token)}
        return Response(data, status=status.HTTP_201_CREATED)

class UserLoginAPIView(GenericAPIView):
    permission_classes = [AllowAny]  # Ensure permission_classes is a list
    authentication_classes = []  # No authentication needed for login
    serializer_class = UserLoginSerializer
    
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']  # Ensure validated data includes 'user'
        custom_serializer = CustomUserSerializer(user)
        token = RefreshToken.for_user(user)
        data = custom_serializer.data
        data["tokens"] = {"refresh": str(token),  
                          "access": str(token.access_token)}
        return Response(data, status=status.HTTP_200_OK)

class UserLogoutAPIView(GenericAPIView):
    permission_classes = [IsAuthenticated]  # Ensure permission_classes is a list
    authentication_classes = [JWTAuthentication]  # Specify JWTAuthentication in a list
    
    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.data.get("refresh")  # Safely access refresh token
            if not refresh_token:
                return Response({"detail": "Refresh token is required."}, status=status.HTTP_400_BAD_REQUEST)
            
            token = RefreshToken(refresh_token)
            token.blacklist()  # Blacklist the refresh token to log the user out
            return Response(status=status.HTTP_205_RESET_CONTENT)
        
        except Exception as e:
            return Response({"detail": str(e)}, status=status.HTTP_400_BAD_REQUEST)

class UserInfoAPIView(RetrieveAPIView):
    permission_classes = [IsAuthenticated]  # Ensure permission_classes is a list
    authentication_classes = [JWTAuthentication]  # Specify JWTAuthentication in a list
    serializer_class = CustomUserSerializer
    
    def get_object(self):
        return self.request.user  # Return the authenticated user object
