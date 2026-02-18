from rest_framework import generics, permissions
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
from .services import UserService

# Create your views here.

## User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    throttle_scope = 'auth'
    
## Profile (Current User)
class userProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user

    def perform_update(self, serializer):
        UserService.update_user_profile(self.request.user, serializer.validated_data)