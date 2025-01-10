from django.contrib import admin
from django.urls import path,include
from task.views import *

urlpatterns = [
    # path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('get/', get, name="Get tasks"),
    path('delete/<id>/', delete ,name="Delete Task"),
    path('update/<id>/', update ,name="update"),
    path('update_status/<id>/', update_status, name='update_status'),
    path('home/', home ,name="home"),
    
]
