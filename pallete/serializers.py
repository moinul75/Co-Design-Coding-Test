from rest_framework import serializers
from .models import Palette, UserProfile,PaletteRevision

class PaletteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Palette
        fields = '__all__'

class PaletteCreateSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=255)
    dominant_color = serializers.CharField(max_length=7)
    is_public = serializers.BooleanField(default=False)

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ('favorite_palettes', )


class PaletteRevisionSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaletteRevision
        fields = ['id', 'palette', 'user', 'timestamp', 'changes']