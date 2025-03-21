from django.db import models

# Create your models here.
class Page(models.Model):
    title = models.CharField(max_length=100)
    content = models.TextField()
    image = models.CharField(max_length=30)
    last_update = models.DateTimeField(auto_now=True)
    category = models.CharField(max_length=30,default='')
    
    def __str__(self):
        return self.title

    def get_image_path(self):
        return f"img/{self.image}"