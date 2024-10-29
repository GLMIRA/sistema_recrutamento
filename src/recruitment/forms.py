from django import forms
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "password"]


class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(
            attrs={"placeholder": "Username", "class": "form-control"}
        ),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"placeholder": "Password", "class": "form-control"}
        )
    )


class CandidateForm(forms.ModelForm):
    class Meta:
        model = models.Candidate
        fields = [
            "name",
            "birthday",
            "sex",
            "breed",
            "phone",
            "email",
            "url_linkedin",
        ]


class ProfessionalExperienceForm(forms.ModelForm):
    class Meta:
        model = models.ProfessionalExperience
        fields = [
            "position",
            "company",
            "start_date",
            "end_date",
            "description",
        ]


class EducationForm(forms.ModelForm):
    class Meta:
        model = models.Education
        fields = [
            # TODO: PRoblemas com os formularios de criar e editar
            "institution",
            "level",
            "course",
            "start_date",
            "end_date",
        ]
