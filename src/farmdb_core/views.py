from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import FarmerSurveySerializer
# Create your views here.
class TypeFormFarmerSurvey(APIView):
    """
    Receives a TypeForm Farmer Survey response through a webhook and parses it into FarmDB
    """
    def post(self, request, format=None):
        serializer = FarmerSurveySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)