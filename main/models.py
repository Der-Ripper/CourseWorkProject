from django.db import models

# Create your models here.
class Claim(models.Model):
    title = models.CharField(max_length=50)
    description = models.JSONField()
    status = models.CharField(max_length=20)
    claim_number = models.CharField(max_length=20)
    department_name = models.CharField(max_length=50)

    def __str__(self):
        return self.title