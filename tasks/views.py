from rest_framework import generics, permissions, viewsets, filters
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth.models import User
from .models import Task
from .serializers import TaskSerializer, UserSerializer
from rest_framework.authentication import TokenAuthentication

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer

class UserViewSet(viewsets.ModelViewSet):
    """
    Requirement: CRUD operations for users. 
    Users can only manage their own profile data.
    """
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    def get_queryset(self):
        return User.objects.filter(id=self.request.user.id)

class TaskViewSet(viewsets.ModelViewSet):
    """
    Requirement: CRUD for Tasks with Filtering and Sorting.
    """
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [TokenAuthentication]
    
    # Requirement: Filter by Status, Priority, and Due Date.
    # Requirement: Sort by Due Date or Priority Level.
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['status', 'priority', 'due_date']
    ordering_fields = ['due_date', 'priority']

    def get_queryset(self):
        # Requirement: Ensure tasks are only accessible to the users who created them.
        return Task.objects.filter(owner=self.request.user)

    def perform_create(self, serializer):
        # Requirement: Task Ownership.
        serializer.save(owner=self.request.user)