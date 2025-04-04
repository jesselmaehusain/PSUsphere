from django.forms import ModelForm # type: ignore
from django import forms # type: ignore
from .models import Organization # type: ignore

class OrganizationForm(ModelForm):
    class Meta:
        model = Organization
        fields = "__all__"