from django.http.response import JsonResponse
from django.shortcuts import render
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, authentication, permissions
from .serializers import PersonToRoleToOrgSerializer
from .utils.survey.parser import parse_survey
from base64 import b64encode
from hashlib import sha256
import hmac
from django.conf import settings
#import settings

# Create your views here.
class TypeFormFarmerSurvey(APIView):
    """
    Receives a TypeForm Farmer Survey response through a webhook and parses it into FarmDB
    """
    authentication_classes = []
    permission_classes = [permissions.AllowAny]

    def get(self, request, pk, format=None):
        return None


    def post(self, request, format=None):
        if valid_typeform_signature(request):
            parsed_data = parse_survey(request.data)
            #TODO: try/except to store request body and stacktrace to debug db table
            serializer = PersonToRoleToOrgSerializer(data=parsed_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


def valid_typeform_signature(request):
    api_signature = request.META.get('HTTP_TYPEFORM_SIGNATURE')
    secret = settings.FARMDB_CORE_TYPEFORM_SECRET
    computed_sig = hmac.new(
        secret.encode('utf-8'),
        msg=request.body, digestmod=sha256
    ).digest()
    signature = 'sha256=' + b64encode(computed_sig).decode()
    return api_signature == signature