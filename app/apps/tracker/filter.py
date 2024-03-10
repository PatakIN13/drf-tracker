from django_filters import rest_framework as filters
from .models import UsersTask, Task


class TaskFilter(filters.FilterSet):
    created = filters.DateFromToRangeFilter()

    class Meta:
        model = Task
        fields = ['description', 'activity']


class UsersTaskFilter(filters.FilterSet):

    class Meta:
        model = UsersTask
        fields = ['fullname', 'email']
