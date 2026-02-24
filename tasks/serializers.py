from rest_framework import serializers
from .models import Task
from django.contrib.auth.models import User
from django.utils import timezone

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'
        read_only_fields = ['owner', 'created_at', 'completed_at']

    def validate(self, data):
        """
        Enforce submission requirements for data validation.
        """
        
        # 1. Validation: Ensure Due Date is in the future
        # We check 'due_date' only if it's being provided in the request
        if 'due_date' in data and data['due_date'] < timezone.now():
            raise serializers.ValidationError({"due_date": "The due date must be in the future."})

        # 2. Logic: Locking completed tasks
        # self.instance refers to the task already in the database (if this is an update)
        if self.instance and self.instance.status == 'Completed':
            # Check if the user is trying to change fields OTHER than 'status'
            # We allow them to change 'status' back to 'Pending' to unlock it.
            restricted_fields = ['title', 'description', 'due_date', 'priority']
            if any(field in data for field in restricted_fields):
                # If they are NOT changing status to Pending, block the edit
                if data.get('status') != 'Pending':
                    raise serializers.ValidationError(
                        "This task is marked as Completed and is locked. "
                        "Change status to 'Pending' to enable editing."
                    )
        
        return data