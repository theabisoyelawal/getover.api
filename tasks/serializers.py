from rest_framework import serializers
from .models import Task
from django.utils import timezone

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['user', 'created_at', 'completed_at']

    def validate_due_date(self, value):
        # Validation: Due date must be in the future
        if value < timezone.now():
            raise serializers.ValidationError("The due date must be in the future.")
        return value