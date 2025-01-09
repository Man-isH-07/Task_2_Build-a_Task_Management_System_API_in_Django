from django.shortcuts import render,redirect
from .models import Task
from django.http import HttpResponse
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

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
        )

        return redirect('/home')

    queryset = Task.objects.all()
    context = {'tasks' : queryset}
    
    return render(request,'index.html',context)

#Update

      
def update(request,id):    #Support partial edits
    queryset = Task.objects.get(id=id)

    if request.method == "POST":
        data = request.POST
        title = data.get("title")
        description = data.get("description")
        task_type = data.get("task_type")
    
        queryset.title=title
        queryset.description=description
        queryset.task_type=task_type

        queryset.save()
        return redirect('/home')
    
    context = {'tasks' : queryset}
    
    return render(request,'update_task.html',context)


#Delete

def delete(request,id):
            queryset = Task.objects.get(id=id)
            queryset.delete()
            return HttpResponse({
                "Data Deleted."
            }, status=status.HTTP_200_OK)
 




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
    

    


    
        