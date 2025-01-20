from django.contrib import admin
from django.urls import path,include
from task.views import *

urlpatterns = [
    # path('api/', include('api.urls')),
    path('admin/', admin.site.urls),
    path('login/',login_page,name="login_page"),
    path('register/',register_page,name="register_Page"),
    path('logout/', logout_view, name='logout_view'),
    path('get/', get, name="Get tasks"),
    path('delete/<id>/', delete ,name="Delete Task"),
    path('update/<id>/', update ,name="update"),
    path('update_status/<id>/', update_status, name='update_status'),
    path('home/', home ,name="home"),
    path('ui/',UserInterface,name="UserInterface"),
    path('view_session/', view_session, name='view_session'),
    path('trigger-task/', trigger_task, name='trigger_task'),
    path('sent_mail',send_mail_to_all,name="send_mail_to_all") 
]
