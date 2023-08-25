from django.db import models
from django.contrib.auth.models import User

class Palette(models.Model):
    name = models.CharField(max_length=255)
    dominant_colors = models.JSONField()
    accent_colors = models.JSONField()
    is_public = models.BooleanField(default=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    favorite_palettes = models.ManyToManyField(Palette, related_name='favorited_by')

    def __str__(self):
        return self.user.username
    
class PaletteRevision(models.Model):
    palette = models.ForeignKey(Palette, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Use CASCADE instead of SET_NULL
    timestamp = models.DateTimeField(auto_now_add=True)
    changes = models.TextField()