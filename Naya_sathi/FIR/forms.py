from django import forms
from django.forms import formset_factory
from .models import FIRReport, EvidenceImage

class FIRReportForm(forms.ModelForm):
    class Meta:
        model = FIRReport
        fields = ['name', 'address', 'email', 'contact', 'subject', 'custom_subject', 'description', 'passport_photo', 'citizenship_front', 'citizenship_back']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter your complete address',
                'required': True
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email address',
                'required': True
            }),
            'contact': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your contact number',
                'required': True
            }),
            'subject': forms.Select(attrs={
                'class': 'form-control',
                'id': 'id_subject',
                'required': True
            }),
            'custom_subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Please specify the subject',
                'id': 'id_custom_subject',
                'style': 'display: none;'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 5,
                'placeholder': 'Describe the event/problem in detail',
                'required': True
            }),
            'passport_photo': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'citizenship_front': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'citizenship_back': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            })
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field not in ['passport_photo', 'citizenship_front', 'citizenship_back', 'custom_subject']:
                self.fields[field].required = True
        
        # Make custom_subject not required by default
        self.fields['custom_subject'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        subject = cleaned_data.get('subject')
        custom_subject = cleaned_data.get('custom_subject')
        
        # If subject is 'other', custom_subject is required
        if subject == 'other' and not custom_subject:
            raise forms.ValidationError("Please specify the subject when selecting 'Other'.")
        
        # If subject is not 'other', clear custom_subject
        if subject != 'other':
            cleaned_data['custom_subject'] = ''
            
        return cleaned_data

class EvidenceImageForm(forms.ModelForm):
    class Meta:
        model = EvidenceImage
        fields = ['image', 'description']
        widgets = {
            'image': forms.FileInput(attrs={
                'class': 'form-control',
                'accept': 'image/*'
            }),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Brief description of this evidence (optional)'
            })
        }

# Create a formset for multiple evidence images
EvidenceImageFormSet = formset_factory(EvidenceImageForm, extra=1, can_delete=True)