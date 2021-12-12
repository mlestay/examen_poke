from django.db import models
from django.db.models.fields.related import ForeignKey

# Create your models here.
class User(models.Model):
    name = models.CharField(max_length=120, null=False, blank=False)
    alias = models.CharField(max_length=20, null=False, blank=False)
    email = models.EmailField()
    password = models.CharField(max_length=255, null=False, blank=False)
    dob = models.DateField(null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Poke(models.Model):
    Poke_it = models.ForeignKey(User, related_name = 'poke_usuario', on_delete = models.CASCADE, null=True)
    poke_list = models.ManyToManyField(User, related_name="pokess")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
