from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save

# Create your models here.

#USER MODEL FROM DJANGO LINKED WITH THIS MODEL
class UserProfile(models.Model):
    """Extends default user of django and add new attributes to check."""
    user = models.OneToOneField(User,on_delete=models.CASCADE)#uses user created by django
    count_journals = models.PositiveBigIntegerField(default=0)
    journal_limit = models.PositiveIntegerField(default=5)
    pages_per_journal_limit = models.PositiveBigIntegerField(default=15)

    def add_journal(self,quantity):
        self.count_journals += quantity
        self.save()
    
    def sub_journal(self,quantity):
        self.count_journals -= quantity
        self.save()

    def __str__(self):
        return self.user.username

def create_profile(sender, **kwargs):
    """Creates profile for new user."""
    if kwargs['created']:
        user_profile = UserProfile.objects.create(user=kwargs['instance'])

post_save.connect(create_profile, sender=User)