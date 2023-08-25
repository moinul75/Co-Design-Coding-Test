from django.shortcuts import render,get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .serializers import PaletteCreateSerializer, PaletteSerializer,PaletteRevisionSerializer
from .models import Palette,UserProfile,PaletteRevision
import random
from django.db.models import Q
from urllib.parse import unquote

#public color palettes without login
@api_view(['GET'])
def public_palettes(request):
    public_palettes = Palette.objects.filter(is_public=True)
    serializer = PaletteSerializer(public_palettes, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_palette(request):
    serializer = PaletteCreateSerializer(data=request.data)
    if serializer.is_valid():
        name = serializer.validated_data['name']
        dominant_color = serializer.validated_data['dominant_color']
        is_public = serializer.validated_data['is_public']

        # Generate accent colors
        accent_colors = generate_accent_colors()

        # Create and save the palette
        palette = Palette(
            name=name,
            dominant_colors=[dominant_color],
            accent_colors=accent_colors,
            is_public=is_public,
            creator=request.user
        )
        palette.save()

        # Serialize and return the palette data
        palette_serializer = PaletteSerializer(palette)
        return Response(palette_serializer.data, status=201)

    return Response(serializer.errors, status=400)

def generate_accent_colors(num_colors=4):
    accent_colors = []
    for _ in range(num_colors):
        accent_colors.append(generate_random_color())
    return accent_colors

def generate_random_color():
    return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def update_palette(request, palette_id):
    try:
        palette = Palette.objects.get(id=palette_id, creator=request.user)
    except Palette.DoesNotExist:
        return Response({"detail": "Palette not found or you don't have permission."}, status=404)

    serializer = PaletteCreateSerializer(palette, data=request.data, partial=True)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data)

    return Response(serializer.errors, status=400)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def save_to_favorites(request, palette_id):
    try:
        palette = Palette.objects.get(id=palette_id)
    except Palette.DoesNotExist:
        return Response({"detail": "Palette not found."}, status=404)

    user_profile, created = UserProfile.objects.get_or_create(user=request.user)
    user_profile.favorite_palettes.add(palette)
    return Response({"detail": "Palette added to favorites."}, status=201)


#search by name and dominant colors 
@api_view(['GET'])
def search_palettes(request):
    search_query = unquote(request.GET.get('query', ''))  # Decode the URL-encoded query parameter
    palettes = Palette.objects.filter(Q(name__icontains=search_query) | Q(dominant_colors__icontains=search_query) , is_public=True)
    serializer = PaletteSerializer(palettes, many=True)
    return Response(serializer.data)


#revision history 
@api_view(['GET'])
def get_palette_revisions(request, palette_id):
    palette = get_object_or_404(Palette, id=palette_id)
    revisions = PaletteRevision.objects.filter(palette=palette)
    serializer = PaletteRevisionSerializer(revisions, many=True)
    return Response(serializer.data)