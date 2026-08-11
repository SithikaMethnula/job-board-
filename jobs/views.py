from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_framework import status
from .models import Job
from .serializers import JobSerializer

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticatedOrReadOnly])
def job_list_create(request):
    if request.method == 'GET':
        jobs = Job.objects.all()
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)

    elif request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(employer=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
@permission_classes([IsAuthenticatedOrReadOnly])
def job_detail(request, pk):
    try:
        job = Job.objects.get(pk=pk)
    except Job.DoesNotExist:
        return Response({'error': 'Job not found'}, status=status.HTTP_404_NOT_FOUND)

   
    if request.method == 'GET':
        serializer = JobSerializer(job)
        return Response(serializer.data)

    
    elif request.method == 'PUT':
        
        if job.employer != request.user:
            return Response({'error': 'You do not have permission to edit this job'}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = JobSerializer(job, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    
    elif request.method == 'DELETE':
        if job.employer != request.user:
            return Response({'error': 'You do not have permission to delete this job'}, status=status.HTTP_403_FORBIDDEN)
        
        job.delete()
        return Response({'message': 'Job deleted successfully'}, status=status.HTTP_204_NO_CONTENT)