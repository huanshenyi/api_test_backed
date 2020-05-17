from django.shortcuts import render
from rest_framework import viewsets
from .models import Project
from rest_framework.permissions import IsAuthenticated
from .serializers import ProjectSerializer


class ProjectViewSets(viewsets.ModelViewSet):
    queryset = Project.objects.all()
    permission_classes = [IsAuthenticated, ]
    serializer_class = ProjectSerializer

