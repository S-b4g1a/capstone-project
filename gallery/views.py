from django.shortcuts import render
from .models import Gallery
# Create your views here.

def gallery(request, hotel_id):
    images = Gallery.objects.filter(hotel_id=hotel_id)
    return render(request, 'gallery.html', {'images': images})
