from datetime import datetime, timedelta

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import ListAPIView

from .filter import TaskFilter
from .models import UsersTask, Task
from .serializers import UsersSerializer, TaskSerializer, UsersTaskSerializer, UserTasksSerializer, UserTasksWeekSerializer


# Create your views here.
class UsersView(ModelViewSet):
    queryset = UsersTask.objects.all()
    serializer_class = UsersSerializer
    filter_backends = [DjangoFilterBackend]

    def create(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = UsersSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @classmethod
    def date_to_datetime(cls, user, start_date, end_date, format_string='%Y-%m-%d'):
        if start_date and end_date:
            start_date = datetime.strptime(start_date, format_string)
            end_date = datetime.strptime(end_date, format_string)
            start_date = datetime(start_date.year, start_date.month, start_date.day, 0, 0, 0)
            end_date = datetime(end_date.year, end_date.month, end_date.day, 23, 59, 59)

            tasks = Task.objects.filter(user=user, created__gte=start_date, created__lte=end_date).order_by('-activity')
        else:
            tasks = Task.objects.filter(user=user).order_by('-activity')
        return tasks

    @action(detail=True, methods=['get'], url_path='tasks/(?P<start_date>[^/.]+)&(?P<end_date>[^/.]+)?')
    def tasks(self, request, pk=None, start_date=None, end_date=None, format_string='%Y-%m-%d'):
        user = self.get_object()
        tasks = self.date_to_datetime(user, start_date, end_date, format_string)

        serializer = UserTasksSerializer(tasks, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(detail=True, methods=['get'], url_path='tasks/week/(?P<start_date>[^/.]+)&(?P<end_date>[^/.]+)?')
    def tasks_week(self, request, pk=None, start_date=None, end_date=None, format_string='%Y-%m-%d'):
        user = self.get_object()
        tasks = self.date_to_datetime(user, start_date, end_date, format_string)

        serializer = UserTasksWeekSerializer(tasks, context={'week': 0}, many=True)
        return Response({'week': str(timedelta(minutes=serializer.data[-1]))}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['delete'])
    def destroy_all_tasks(self, request, pk=None):
        user = self.get_object()
        tasks = Task.objects.filter(user=user)
        tasks.delete()
        return Response({'message': 'All tasks deleted'}, status=status.HTTP_204_NO_CONTENT)


class TaskView(ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = TaskFilter

    def create(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request, *args, **kwargs):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request, *args, **kwargs):
        return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(detail=True, methods=['post'])
    def start_activity(self, request, pk=None):
        task = self.get_object()
        task.start_activity_time = datetime.now()
        task.save()
        return Response({'message': 'Activity started'}, status=status.HTTP_200_OK)

    @action(detail=True, methods=['post'])
    def stop_activity(self, request, pk=None):
        task = self.get_object()
        end_activity_time = datetime.now()
        start_activity_time = datetime.strptime(str(task.start_activity_time), '%Y-%m-%d %H:%M:%S+00:00')
        task.activity = task.activity + ((end_activity_time - start_activity_time).seconds // 60)
        task.start_activity_time = None
        task.save()
        return Response({'message': 'Activity stopped'}, status=status.HTTP_200_OK)


class UsersAllTasksView(ListAPIView):
    serializer_class = UsersTaskSerializer
    queryset = UsersTask.objects.all()

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        response.data = {'count': len(response.data), 'users': response.data}
        return response
