from django.contrib import admin
from .models import Room, Facility, Booking, ContactMessage, Gallery, Complaint


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = (
        'room_number',
        'room_type',
        'rent',
        'capacity',
        'available',
    )
    list_filter = ('room_type', 'available')
    search_fields = ('room_number',)


@admin.register(Facility)
class FacilityAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'room',
        'check_in_date',
        'number_of_occupants',
        'status',
    )
    list_filter = ('status',)
    search_fields = ('user__username', 'room__room_number')


@admin.register(ContactMessage)
class ContactMessageAdmin(admin.ModelAdmin):
    list_display = (
        'name',
        'email',
        'subject',
        'created_at',
    )
    search_fields = (
        'name',
        'email',
        'subject',
    )
    list_filter = ('created_at',)


@admin.register(Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title',)
    search_fields = ('title',)
@admin.register(Complaint)
class ComplaintAdmin(admin.ModelAdmin):
    list_display = (
        'user',
        'subject',
        'created_at',
        'status',
    )

    list_filter = ('status', 'created_at')

    search_fields = (
        'user__username',
        'subject',
        'description',
    )