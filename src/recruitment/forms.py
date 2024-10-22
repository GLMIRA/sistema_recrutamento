from django import forms
from . import models


class CandidateForm(forms.ModelForm):
    class Meta:
        model = models.Candidate
        fields = ["name", "birthday", "sex", "breed", "phone", "email", "url_linkedin"]
