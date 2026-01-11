from django.db import models


class DetectionLog(models.Model):
    """Log of spam detection predictions"""
    created_at = models.DateTimeField(auto_now_add=True)
    email = models.EmailField()
    content = models.TextField()
    prediction = models.CharField(max_length=10)  # spam or ham
    probability = models.FloatField()
    model_used = models.CharField(max_length=50)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.email} - {self.prediction} - {self.created_at}"
