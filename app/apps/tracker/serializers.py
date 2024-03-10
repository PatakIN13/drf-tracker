from datetime import timedelta
from django.db import models

from rest_framework import serializers
from .models import UsersTask, Task


class UsersSerializer(serializers.ModelSerializer):
    class Meta:
        model = UsersTask
        fields = ['id', 'fullname', 'email']

    def create(self, validated_data):
        fullname = validated_data['fullname']
        email = validated_data['email']
        user = UsersTask.objects.create(
            fullname=fullname,
            email=email
        )
        return user

    def update(self, instance, validated_data):
        instance.fullname = validated_data.get('fullname', instance.fullname)
        instance.email = validated_data.get('email', instance.email)
        instance.save()
        return instance


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ['id', 'description', 'activity']

    def create(self, validated_data):
        description = validated_data['description']
        task = Task.objects.create(
            description=description
        )
        return task

    def update(self, instance, validated_data):
        instance.user = validated_data.get('user', instance.user)
        instance.description = validated_data.get('description', instance.description)
        instance.activity = validated_data.get('activity', instance.activity)
        instance.save()
        return instance


class UserTasksSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        result = {response['description']: str(timedelta(minutes=response['activity']))}
        return result


class UserTasksWeekSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = '__all__'

    def to_representation(self, instance):
        response = super().to_representation(instance)
        activity = response['activity']
        self.context['week'] = self.context['week'] + activity
        return self.context['week']


class UsersTaskSerializer(serializers.ModelSerializer):
    TASKS_USER = TaskSerializer(many=True, read_only=True)

    class Meta:
        model = UsersTask
        fields = ['id', 'fullname', 'TASKS_USER']
