from rest_framework import serializers
from . import models
from django.contrib.auth.models import User


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "password",
        ]
        extra_kwargs = {"password": {"write_only": True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validate_data):
        instance.username = validate_data.get("username", instance.username)
        instance.email = validate_data.get("email", instance.email)
        password = validate_data.get("password", None)
        if password:
            instance.set_password(password)
        instance.save()
        return instance


class EducationSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Candidate
        fields = "__all__"


class CandidateSerializer(serializers.ModelSerializer):

    educations = EducationSerializer(many=True, read_only=True)

    class Meta:
        model = models.Candidate
        fields = "__all__"
