from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class FIRReport(models.Model):
    SUBJECT_CHOICES = [
        ('murdering', 'Murdering'),
        ('sexual_harassment', 'Sexual Harassment'),
        ('corruption', 'Corruption'),
        ('miss_behave', 'Miss-behave'),
        ('cyber_crime', 'Cyber Crime'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in valid format")]
    )
    subject = models.CharField(max_length=20, choices=SUBJECT_CHOICES, default='other')
    custom_subject = models.CharField(max_length=100, blank=True, null=True)
    description = models.TextField()
    evidence_image = models.ImageField(upload_to='fir_evidence/', blank=True, null=True)
    passport_photo = models.ImageField(upload_to='fir_photos/', blank=True, null=True)
    citizenship_front = models.ImageField(upload_to='fir_citizenship/', blank=True, null=True)
    citizenship_back = models.ImageField(upload_to='fir_citizenship/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def get_subject_display_name(self):
        if self.subject == 'other' and self.custom_subject:
            return self.custom_subject
        return self.get_subject_display()
    
    def __str__(self):
        return f"FIR Report by {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']

class EvidenceImage(models.Model):
    fir_report = models.ForeignKey(FIRReport, related_name='evidence_images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='fir_evidence/')
    description = models.CharField(max_length=200, blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Evidence for FIR {self.fir_report.id} - {self.uploaded_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['uploaded_at']
