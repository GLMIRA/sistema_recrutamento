from rest_framework import viewsets, permissions
from . import serializers
from . import models


class CandidateViewSet(viewsets.ModelViewSet):
    queryset = models.Candidate.objects.all()
    serializer_class = serializers.CandidateSerializer
    permission_classes = [permissions.IsAuthenticated]
