from django import forms
from . import models


class CandidateForm(forms.ModelForm):
    class Meta:
        model = models.Candidate
        fields = ["name", "birthday", "sex", "breed", "phone", "email", "url_linkedin"]


class ProfessionalExperienceForm(forms.ModelForm):
    class Meta:
        model = models.ProfessionalExperience
        fields = [
            "candidate",
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
            "candidate",
            "institution",
            "level",
            "course",
            "start_date",
            "end_date",
        ]
