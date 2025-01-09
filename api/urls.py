from django.urls import path,include
from task import views
urlpatterns = [
    path('home/',views.home),
    # path('tasks/',views.TaskAPI.as_view())
]
