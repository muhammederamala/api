from django.db import models

# Create your models here.
class certificate_model(models.Model):
	title = models.CharField(max_length=40)
	name = models.CharField(max_length=40)
	subtitle = models.CharField(max_length=255)
	date = models.DateField()
	signature = models.CharField(max_length=10)
	certificate_file = models.ImageField(upload_to='certificates')