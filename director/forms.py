from django import forms
from location_field.forms.plain import PlainLocationField

from .models import CameraModel


class CameraForm(forms.ModelForm):
    camera_name = forms.CharField(max_length=50, required=True)
    web_address = forms.CharField(max_length=100, required=True)
    city = forms.CharField(max_length=40, required=True)
    location = PlainLocationField(based_fields=['city'],
                                  initial='41.311081,69.240562', zoom=10, required=True)

    class Meta:
        model = CameraModel
        fields = ['camera_name', 'web_address', 'city', 'location']
