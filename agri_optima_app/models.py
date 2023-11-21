from django.db import models

# Create your models here.
class UserInfo(models.Model):
    uname = models.CharField(max_length=200)
    profile_pic = models.ImageField(upload_to='agri_optima_app/profile_pic' , null= True, blank=True)

    def __str__(self):
        return self.uname
    
class SoilImage(models.Model):
    image = models.ImageField(upload_to='soil_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Soil Image {self.id}"

class PlantImage(models.Model):
    image = models.ImageField(upload_to='plant_images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Plant Image {self.id}"