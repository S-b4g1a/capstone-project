from django.db import models

# Create your models here.

class Hotel(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    description = models.TextField()
    image = models.ImageField(upload_to='hotels/')

class Room(models.Model):
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_type = models.CharField(max_length=50)
    price_per_night = models.DecimalField(max_digits=10, decimal_places=2)
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.room_type} - {self.hotel.name} (${self.price_per_night}/night)"

class Booking(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    check_in = models.DateField()
    check_out = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.0)
    confirmed = models.BooleanField(default=False)

    def calculate_total_price(self):
        """Calculate total price based on the number of nights."""
        nights = (self.check_out - self.check_in).days
        return self.room.price_per_night * nights

class RoomGallery(models.Model):
    room = models.ForeignKey(Room, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='room_gallery/')
    caption = models.CharField(max_length=100, blank=True)



