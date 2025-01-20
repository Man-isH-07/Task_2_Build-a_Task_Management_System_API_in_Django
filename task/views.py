from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth import login,logout
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.cache import cache  # Import Django's cache system
from datetime import datetime


# # Create your views here.
@api_view(['GET','POST','DELETE'])

def get(request):
    queryset = Task.objects.all().order_by('-pk')  # Fetch all records, ordered by descending primary key
    serializer = TaskSerializer(queryset, many=True)  # Serialize all tasks
    return Response(serializer.data) 


def login_page(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        # Check if the user exists
        if not User.objects.filter(username=username).exists():
            messages.error(request, "User not registered.")
            return redirect('/login/')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)  # Logs in the user and creates a session
            print(f"Session Key after login: {request.session.session_key}")
            return redirect('/ui/')  # Redirect to the desired page
        else:
            messages.error(request, "Invalid username or password")
    
    return render(request, 'login.html')

def register_page(request):
     if request.method == 'POST':
          first_name = request.POST.get('first_name')
          last_name = request.POST.get('last_name')
          email=request.POST.get('email')
          username = request.POST.get('username')
          password = request.POST.get('password')
          
          user = User.objects.filter(username=username)
          if user.exists():
               messages.info(request, "Username already taken.")
               return redirect('/register/')
          
          user = User.objects.create(
               first_name = first_name,
               last_name = last_name,
               username = username,
               email = email,
          )
          user.set_password(password)
          user.save()
          messages.success(request, "Account created successfully.")

          return redirect('/register/')

     return render(request,'register.html')

def logout_view(request):
    logout(request)  # Deletes the session in Redis
    return redirect('login_page')

@login_required
def UserInterface(request):
     user=request.user
     return render(request,'UserInterface.html')

from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.utils.timezone import now
from datetime import datetime
from django.core.cache import cache
from .models import Task
from task.tasks import refresh_task_cache


def home(request):
    today = now()

    if request.method == "POST":
        title = request.POST.get("title")
        description = request.POST.get("description")
        task_type = request.POST.get("task_type")
        scheduled_date = request.POST.get("scheduled_date")


        # Parse scheduled_date only if it exists and is valid
        if scheduled_date:
            try:
                scheduled_date = datetime.strptime(scheduled_date, "%Y-%m-%dT%H:%M")
            except ValueError:
                return HttpResponse("Invalid date format. Please use YYYY-MM-DDTHH:MM format.", status=400)
        else:
            scheduled_date = None

        from django.utils.timezone import make_aware

        # Ensure scheduled_date is timezone-aware
        if scheduled_date and isinstance(scheduled_date, datetime) and scheduled_date.tzinfo is None:
            scheduled_date = make_aware(scheduled_date)

        current_time = now()
        
        if scheduled_date and scheduled_date > today:
            task_status = "Scheduled"
        else:
            task_status = "Ongoing"

        # Create the task
        task = Task.objects.create(
            title=title,
            description=description,
            task_type=task_type,
            status=task_status,
            scheduled_date=scheduled_date,
            user=request.user,
        )
        refresh_task_cache.apply_async(args=[request.user.id], countdown=30)

        # Update the cache
        ongoing_tasks = cache.get(f"ongoing_tasks_{request.user.id}")
        scheduled_tasks = cache.get(f"scheduled_tasks_{request.user.id}")

        if ongoing_tasks is not None and task_status == "Ongoing":
            ongoing_tasks = list(ongoing_tasks)
            ongoing_tasks.insert(0, task)
            cache.set(f"ongoing_tasks_{request.user.id}", ongoing_tasks, timeout=3600)

        if scheduled_tasks is not None and task_status == "Scheduled":
            scheduled_tasks = list(scheduled_tasks)
            scheduled_tasks.insert(0, task)
            cache.set(f"scheduled_tasks_{request.user.id}", scheduled_tasks, timeout=3600)

        return redirect('/home/')

    # Fetch tasks from cache or database
    ongoing_tasks = cache.get(f"ongoing_tasks_{request.user.id}")
    completed_tasks = cache.get(f"completed_tasks_{request.user.id}")
    scheduled_tasks = cache.get(f"scheduled_tasks_{request.user.id}")

    if not ongoing_tasks or not completed_tasks or not scheduled_tasks:
        ongoing_tasks = Task.objects.filter(user=request.user, status="Ongoing").order_by('-id')
        completed_tasks = Task.objects.filter(user=request.user, status="Completed").order_by('-id')
        scheduled_tasks = Task.objects.filter(user=request.user, status="Scheduled", scheduled_date__gte=today)

        # Cache the results
        cache.set(f"ongoing_tasks_{request.user.id}", ongoing_tasks, timeout=3600)
        cache.set(f"completed_tasks_{request.user.id}", completed_tasks, timeout=3600)
        cache.set(f"scheduled_tasks_{request.user.id}", scheduled_tasks, timeout=3600)

    context = {
        'ongoing_tasks': ongoing_tasks,
        'completed_tasks': completed_tasks,
        'scheduled_tasks': scheduled_tasks,
        'user': request.user,
    }

    return render(request, 'index.html', context)

from django.http import JsonResponse
from task.tasks import add
def trigger_task(request):
    result = add.delay(10, 20)  
    return JsonResponse({"task_id": result.id, "status": "Task submitted"})

from task.tasks import send_weekly_report
def send_mail_to_all(request):
    send_weekly_report.delay()
    return HttpResponse('Sent')


def view_session(request):
    session_data = request.session.items()
    print("Session Key:", request.session.session_key)
    return JsonResponse(dict(session_data))  # Return session data as JSON


#Update

def update(request, id):  # Support partial edits
    task = get_object_or_404(Task, id=id)  # Fetch the task object

    if request.method == "POST":
        # Extract form data
        title = request.POST.get("title")
        description = request.POST.get("description")
        task_type = request.POST.get("task_type")

        # Update the task object
        if title:
            task.title = title
        if description:
            task.description = description
        if task_type:
            task.task_type = task_type

        task.save()  # Save the changes to the database

        cache.delete(f"ongoing_tasks_{request.user.id}")
        cache.delete(f"completed_tasks_{request.user.id}")

        return redirect('home')  # Redirect to the home page or task list

    return render(request, 'update_task.html', {'task': task})

#Delete

def delete(request,id):
            queryset = Task.objects.get(id=id)
            queryset.delete()
            HttpResponse({ "Deleted"
            }, status=status.HTTP_200_OK)

            cache.delete(f"ongoing_tasks_{request.user.id}")
            cache.delete(f"completed_tasks_{request.user.id}")

            return redirect('home')
            
 
# View to update task status
from django.utils.timezone import now

def update_status(request, id):
    task = get_object_or_404(Task, id=id)

    # Toggle status
    if task.status == 'Ongoing':
        task.status = 'Completed'
        task.updated_at = now()  # Update timestamp for completion
    else:
        task.status = 'Ongoing'

    task.save()

    cache.delete(f"ongoing_tasks_{request.user.id}")
    cache.delete(f"completed_tasks_{request.user.id}")

    return redirect('home')


# class TaskAPI(APIView):
#     def get(self,request):
#         queryset = Task.objects.all().order_by('-pk')
#         serializer = TaskSerializer(queryset,many=True)

#         return Response( serializer.data)
    
#     def post(self,request):
#         data = request.data
#         serializer=TaskSerializer(data=data)
#         if not serializer.is_valid():
#             return Response({
#             "message" : "Data is not saved.",
#             "errors" : serializer.errors,        
#             })
        
#         serializer.save()
#         return Response({
#             "message" : "Data is saved."            
#         })

    # def put(self,request):
    #     return Response({
    #         "message" : "This is a put method"            
    #     })    