from rest_framework import viewsets, permissions
from rest_framework.response import Response
from . import serializers
from . import models
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = serializers.UserSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return User.objects.filter(is_staff=False, is_superuser=False)

    def retrieve(self, request, *args, **kwargs):
        instance = get_object_or_404(self.get_queryset(), pk=kwargs.get("pk"))
        serializer = self.get_serializer(instance)
        return Response(serializer.data)


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = models.Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    # permission_classes = [permissions.IsAuthenticated]


class EducationViewSet(viewsets.ModelViewSet):
    # queryset = models.Education.objects.all()
    serializer_class = serializers.EducationSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        print(self.kwargs["candidate_pk"])
        print(models.Education.objects.filter(candidate=self.kwargs["candidate_pk"]))
        return models.Education.objects.filter(candidate=self.kwargs["candidate_pk"])

    # def performe_create(self, serializer):
    #     candidate_id = self.kwargs.get("candidate_pk")
    #     candidate = get_object_or_404(models.Candidate.objects.get(pk=candidate_id))
    #     serializer.save(candidate=candidate)
