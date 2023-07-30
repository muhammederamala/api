from django import forms
from .models import certificate_model

class certificate_form(forms.ModelForm):
    class Meta:
        model = certificate_model
        fields = ('title', 'name', 'subtitle', 'date', 'signature', 'certificate_file')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['certificate_file'].required = False
