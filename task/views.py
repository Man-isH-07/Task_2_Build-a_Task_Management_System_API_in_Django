from django.shortcuts import render,redirect,get_object_or_404
from .models import Task
from django.http import HttpResponse,JsonResponse
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from django.contrib.auth import login
import json

# # Create your views here.
@api_view(['GET','POST','DELETE'])

def get(request):
    queryset = Task.objects.all().order_by('-pk')  # Fetch all records, ordered by descending primary key
    serializer = TaskSerializer(queryset, many=True)  # Serialize all tasks
    return Response(serializer.data) 

def home(request):
    
    if request.method=="POST":
        data = request.POST
        title = data.get("title")
        description = data.get("description")
        task_type = data.get("task_type")

        print(data)

        Task.objects.create(
            title=title,
            description=description,
            task_type=task_type,
            status="Ongoing"
        )

        return redirect('/home')

    queryset = Task.objects.all()
    context = {'tasks' : queryset}
    
    return render(request,'index.html',context)

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
        return redirect('home')  # Redirect to the home page or task list

    return render(request, 'update_task.html', {'task': task})

#Delete

def delete(request,id):
            queryset = Task.objects.get(id=id)
            queryset.delete()
            return HttpResponse({ "Deleted"
            }, status=status.HTTP_200_OK)
 
# View to update task status
def update_status(request,id):
    task = get_object_or_404(Task, id=id)
    # Toggle status
    task.status = 'Ongoing' if task.status == 'Completed' else 'Completed'
    task.save()
    # Redirect back to the tasks list page (or where you want)
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