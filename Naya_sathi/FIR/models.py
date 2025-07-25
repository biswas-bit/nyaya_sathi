from django.db import models
from django.core.validators import EmailValidator, RegexValidator

class FIRReport(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    email = models.EmailField(validators=[EmailValidator()])
    contact = models.CharField(
        max_length=15,
        validators=[RegexValidator(regex=r'^\+?1?\d{9,15}$', message="Phone number must be entered in valid format")]
    )
    description = models.TextField()
    evidence_image = models.ImageField(upload_to='fir_evidence/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"FIR Report by {self.name} - {self.created_at.strftime('%Y-%m-%d %H:%M')}"
    
    class Meta:
        ordering = ['-created_at']
