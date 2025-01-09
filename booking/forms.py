# forms.py
from django import forms
from .models import Booking
from datetime import date

class RoomBookingForm(forms.ModelForm):
    class Meta:
        model = Booking
        fields = ['name', 'email', 'phone', 'check_in', 'check_out']
        widgets = {
            'check_in': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
            'check_out': forms.DateInput(attrs={'type': 'date', 'min': date.today().isoformat()}),
        }

    def clean(self):
        cleaned_data = super().clean()
        check_in = cleaned_data.get('check_in')
        check_out = cleaned_data.get('check_out')

        if check_in and check_out:
            if check_in >= check_out:
                raise forms.ValidationError("Check-out date must be after check-in date")

            # Check if room is available for the selected dates
            room = self.initial.get('room')
            if room:
                conflicting_bookings = Booking.objects.filter(
                    room=room,
                    check_in__lte=check_out,
                    check_out__gte=check_in,
                    confirmed=True
                ).exists()

                if conflicting_bookings:
                    raise forms.ValidationError("Room is not available for the selected dates")

        return cleaned_data

# views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .models import Room, Booking
from .forms import RoomBookingForm

def room_detail(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    gallery_images = room.images.all()
    
    context = {
        'room': room,
        'gallery_images': gallery_images,
    }
    return render(request, 'hotels/room_detail.html', context)

def book_room(request, room_id):
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomBookingForm(request.POST, initial={'room': room})
        if form.is_valid():
            booking = form.save(commit=False)
            booking.room = room
            booking.total_price = booking.calculate_total_price()
            booking.save()
            
            messages.success(request, 'Booking request submitted successfully!')
            return redirect('booking_confirmation', booking_id=booking.id)
    else:
        form = RoomBookingForm(initial={'room': room})
    
    context = {
        'form': form,
        'room': room,
    }
    return render(request, 'hotels/book_room.html', context)

def booking_confirmation(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, 'hotels/booking_confirmation.html', {'booking': booking})