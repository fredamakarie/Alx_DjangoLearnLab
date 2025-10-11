from django.db import models

# Create your models here.
class Notification(models.Model):
    recipient = models.ForeignKey(User)
    actor = 
    verb = 
    target =
    timestamp = models.DateTimeField()