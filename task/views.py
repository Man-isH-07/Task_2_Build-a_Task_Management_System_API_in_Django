from django.shortcuts import render
from .models import Task
from rest_framework.response import Response
from .serializers import TaskSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView

# Create your views here.

@api_view(['GET','POST','DELETE'])
def get_task(request):
    queryset = Task.objects.all()
    serializer = TaskSerializer(queryset,many=True)

    return Response( serializer.data)

class TaskAPI(APIView):
    def get(self,request):
        queryset = Task.objects.all().order_by('-pk')
        serializer = TaskSerializer(queryset,many=True)

        return Response( serializer.data)
    
    def post(self,request):
        data = request.data
        serializer=TaskSerializer(data=data)
        if not serializer.is_valid():
            return Response({
            "message" : "Data is not saved.",
            "errors" : serializer.errors,        
            })
        
        serializer.save()
        return Response({
            "message" : "Data is saved."            
        })

    # def put(self,request):
    #     return Response({
    #         "message" : "This is a put method"            
    #     })
    

    # def patch(self,request):    #Support partial edits
    #     data = request.data

    #     if not data.get('id'):
    #         return Response({
    #             "message" : "Data is not uploaded.",
    #             "errors" : "id is required", 
    #         })
        
    #     task = Task.objects.get(id = data.get('id'))
    #     serializer = TaskSerializer(task,data=data,partial=True)
    #     if not serializer.is_valid():
    #         return Response({
    #         "message" : "Data is not saved.",
    #         "errors" : serializer.errors,        
    #         })
        
    #     serializer.save()
    #     return Response({
    #         "message" : "Data is saved."            
    #     })


    def delete(self, request):
        data = request.data

        if not data.get('id'):
            return Response({
                "message": "Data is not deleted.",
                "errors": "id is required"
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            task = Task.objects.get(id=data.get('id'))
            task.delete()
            return Response({
                "message": "Data Deleted.",
                "data": {}
            }, status=status.HTTP_200_OK)
        except Task.DoesNotExist:
            return Response({
                "message": "Task not found.",
                "errors": f"Task with id {data.get('id')} does not exist."
            }, status=status.HTTP_404_NOT_FOUND)
        