from rest_framework import serializers
from . import models


class CandidateSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Candidate
        fields = [
            "name",
            "breed",
        ]
