from django.urls import path 
from .views import public_palettes, create_palette, update_palette, save_to_favorites,search_palettes,get_palette_revisions

urlpatterns = [
    path('public_palettes/', public_palettes, name='public_palettes'),
    path('create_palette/', create_palette, name='create_palette'),
    path('update/<int:palette_id>/', update_palette, name='update_palette'),
    path('save_to_favorites/<int:palette_id>/', save_to_favorites, name='save_favorites'),
    path('search_palettes/', search_palettes, name='search-palettes'),
    path('palettes/<int:palette_id>/revisions/', get_palette_revisions, name='get_palette_revisions'),
]
