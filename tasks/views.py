from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from .models import Task
from .serializers import TaskSerializer

class TaskViewSet(viewsets.ModelViewSet):
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        # Ensure users only see their own tasks
        return Task.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        
        # Logic: Locked if Completed, unless changing back to Pending
        if instance.status == 'Completed':
            new_status = request.data.get('status')
            if new_status != 'Pending':
                return Response(
                    {"error": "This task is completed and locked. Change status to Pending to edit."},
                    status=status.HTTP_400_BAD_REQUEST
                )
        
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        # Logic: Cannot delete completed tasks
        if instance.status == 'Completed':
            return Response(
                {"error": "Completed tasks cannot be deleted."},
                status=status.HTTP_400_BAD_REQUEST
            )
        return super().destroy(request, *args, **kwargs)