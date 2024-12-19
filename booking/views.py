from django.shortcuts import render, get_object_or_404
from .models import Hotel, Room, Booking
from django.core.mail import send_mail
from .models import RoomGallery

def home(request):
    hotels = Hotel.objects.all()
    return render(request, 'home.html', {'hotels': hotels})

def book_room(request, room_id):
    room = get_object_or_404(Room, pk=room_id)
    images = RoomGallery.objects.filter(room=room)
    if request.method == 'POST':
        booking = Booking.objects.create(
            room=room,
            name=request.POST['name'],
            email=request.POST['email'],
            phone=request.POST['phone'],
            check_in=request.POST['check_in'],
            check_out=request.POST['check_out']
        )
        booking.save()

        # Send confirmation email
        send_mail(
            'Booking Confirmation',
            f'Your booking for {room.room_type} is confirmed.',
            'admin@hotelbooking.com',
            [booking.email],
        )

        return render(request, 'confirmation.html', {'booking': booking})
    return render(request, 'book_room.html', {'room': room, 'images': images})




