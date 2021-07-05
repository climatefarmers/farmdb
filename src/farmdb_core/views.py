from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import PersonToRoleToOrgSerializer
from .utils.survey.parser import parse_survey

# Create your views here.
class TypeFormFarmerSurvey(APIView):
    """
    Receives a TypeForm Farmer Survey response through a webhook and parses it into FarmDB
    """

    def get(self, request, pk, format=None):
        return None


    def post(self, request, format=None):
        parsed_data = parse_survey(request.data)
        serializer = PersonToRoleToOrgSerializer(data=parsed_data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)