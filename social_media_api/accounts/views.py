from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from django.contrib.auth import login, logout, get_user_model
from django.shortcuts import get_object_or_404
from .models import CustomUser
from .serializers import RegisterSerializer, LoginSerializer, UserSerializer


# --- Registration ---
class RegisterView(generics.CreateAPIView):
    queryset = get_user_model().objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

   

# --- Login ---
class LoginView(generics.GenericAPIView):
    serializer_class = LoginSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data)

# --- Logout ---
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        # Delete the user’s token to log them out
        request.user.auth_token.delete()
        logout(request)
        return Response({"message": "Successfully logged out."}, status=status.HTTP_200_OK)


# --- Profile ---
class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user


# --- Follow another user ---
class FollowUserView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        follow_user = get_object_or_404(CustomUser, id=user_id)
        if follow_user == request.user:
            return Response({"error": "You cannot follow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.add(follow_user)
        return Response({"message": f"You are now following {follow_user.username}."}, status=status.HTTP_200_OK)


# --- Unfollow another user ---
class UnfollowUserView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, user_id):
        unfollow_user = get_object_or_404(CustomUser, id=user_id)
        if unfollow_user == request.user:
            return Response({"error": "You cannot unfollow yourself."}, status=status.HTTP_400_BAD_REQUEST)
        request.user.followers.remove(unfollow_user)
        return Response({"message": f"You unfollowed {unfollow_user.username}."}, status=status.HTTP_200_OK)
