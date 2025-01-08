from django.urls import path,include
from task import views
urlpatterns = [
    path('get-task/',views.get_task),
    path('tasks/',views.TaskAPI.as_view())
]
