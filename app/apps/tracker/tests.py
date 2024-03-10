from django.test import TestCase
from .models import UsersTask, Task

# Create your tests here.


class TestUsersView(TestCase):
    def test_create(self):
        UsersTask.objects.create(fullname='test',email="test@test.com")
        UsersTask.objects.create(fullname='test2',email="test@asd.com")

    def test_update(self):
        UsersTask.objects.create(fullname='test',email="test@test.net")


class TestTask(TestCase):
    def test_create(self):
        users = UsersTask.objects.get(id=1)
        Task.objects.create(user=users,description='test',activity=1)
        Task.objects.create(user=users,description='test2',activity=2)

    def test_update(self):
        users = UsersTask.objects.get(id=1)
        task = Task.objects.get(id=1)
        task.user = users
        task.description = 'test'
        task.activity = 20
        task.save()

