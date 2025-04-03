from django import forms # type: ignore
from studentorg.models import Organization

class OrganizationForm(forms.ModelForm):
    class Meta:
        model = Organization
        fields = '__all__'  # Include all fields, or specify the ones you need
