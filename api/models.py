from django.db import models
from django.conf import settings

from ckeditor.fields import RichTextField

# Create your models here.
class Journal(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField(max_length=200)
    count_pages = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)#some user

    def add_page(self,quantity):
        self.count_pages += quantity
        self.save()
        
    def sub_page(self,quantity):
        self.count_pages -= quantity
        self.save()
    
    def __str__(self):
        return f"{self.title} |pk: {self.pk}"

class Page(models.Model):
    content = RichTextField(blank=True,null=True,max_length=2000)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    journal = models.ForeignKey(to='Journal',on_delete=models.CASCADE)

    def get_absolute_url(self):
        return f"/api/journals/{self.journal.pk}/pages/{self.pk}/"
    
    def __str__(self):
        return f"Page |pk: {self.pk}"

