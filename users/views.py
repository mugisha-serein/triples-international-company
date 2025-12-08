from rest_framework import generics, permissions
from .models import User
from .serializers import UserRegisterSerializer, UserSerializer
from rest_framework_simplejwt.views import TokenObtainPairView

# Create your views here.

## User Registration View
class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = UserRegisterSerializer
    
## Profile (Current User)
class userProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    
    def get_object(self):
        return self.request.user