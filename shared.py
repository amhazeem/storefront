from django.db import models
from django.utils import timezone

optional = {
    'null' : True,
    'blank': True
}

#functions

def get_random_str():
    import uuid
    return f" {uuid.uuid4()}"



# Models
class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True
