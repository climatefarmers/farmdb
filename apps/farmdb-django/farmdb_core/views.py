import hmac
import json
from base64 import b64encode
from hashlib import sha256

from django.conf import settings
from django.core.serializers import serialize
from django.http import Http404, HttpResponse
from django.http.response import JsonResponse
from django.shortcuts import render
from django.views.generic.base import TemplateView
from rest_framework import authentication, permissions, status
from django.contrib.gis.db.models.functions import Centroid, AsGeoJSON
from rest_framework.response import Response
from rest_framework.views import APIView
from django.views import generic

from .models import Field, Farm
from .serializers import PersonToRoleToOrgSerializer
from .utils.survey.parser import parse_survey



class FarmsView(generic.ListView):
    template_name = "farms.html"
    model = Farm


class FarmDetail(generic.DetailView):
    template_name = "farm_detail.html"
    model = Farm



    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        farm_fields = Field.objects.filter(farm=context['farm'])
        context["geojson"] = json.loads(serialize("geojson", farm_fields))
        print(context)
        return context

class FieldDetail(generic.DetailView):
    template_name = "field_detail.html"
    model = Field

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["geojson"] = json.loads(serialize("geojson", [context['field']]))

        centroid = context['field'].geom.centroid

        context["specs"] = {
            "latitude" : centroid.y,
            "longitude" : centroid.x,
            "area" : round(context['field'].geom.transform('EPSG:3035', clone=True).area / 10000, 2)
        }
        return context

class FieldsMapView(TemplateView):
    """Fields map view."""

    template_name = "map.html"

    def get_context_data(self, **kwargs):
        """Return the view context data."""
        context = super().get_context_data(**kwargs)
        context["fields"] = json.loads(serialize("geojson", Field.objects.all()))
        return context


def index(request):
    return HttpResponse("Hello, world. You're at the FarmDB index.")


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
            # TODO: try/except to store request body and stacktrace to debug db table
            serializer = PersonToRoleToOrgSerializer(data=parsed_data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({}, status=status.HTTP_401_UNAUTHORIZED)


def valid_typeform_signature(request):
    api_signature = request.META.get("HTTP_TYPEFORM_SIGNATURE")
    secret = settings.FARMDB_CORE_TYPEFORM_SECRET
    computed_sig = hmac.new(
        secret.encode("utf-8"), msg=request.body, digestmod=sha256
    ).digest()
    signature = "sha256=" + b64encode(computed_sig).decode()
    return api_signature == signature
