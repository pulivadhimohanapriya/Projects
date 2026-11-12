from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
import random

from .models import Room, Facility, Booking, ContactMessage, Gallery, Complaint
from .forms import RegistrationForm, ComplaintForm


def home(request):
    return render(request, "pg/home.html")


def rooms(request):
    rooms = Room.objects.filter(available=True)
    return render(request, "pg/rooms.html", {"rooms": rooms})


def booking(request, room_id):
    if not request.user.is_authenticated:
        return redirect("login")

    room = Room.objects.get(id=room_id)

    if request.method == "POST":
        check_in_date = request.POST.get("check_in_date")
        number_of_occupants = request.POST.get("number_of_occupants")

        if int(number_of_occupants) > room.capacity:
            messages.error(
                request,
                "Number of occupants cannot exceed room capacity."
            )
            return render(
                request,
                "pg/booking.html",
                {"room": room}
            )

        Booking.objects.create(
            user=request.user,
            room=room,
            check_in_date=check_in_date,
            number_of_occupants=number_of_occupants
        )

        messages.success(
            request,
            "Booking request submitted successfully."
        )

        return redirect("dashboard")

    return render(
        request,
        "pg/booking.html",
        {"room": room}
    )


def room_detail(request, room_id):
    room = Room.objects.get(id=room_id)
    return render(request, "pg/room_detail.html", {"room": room})


def about(request):
    return render(request, "pg/about.html")


def facilities(request):
    facilities = Facility.objects.all()
    return render(request, "pg/facilities.html", {"facilities": facilities})


def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        ContactMessage.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message
        )

        messages.success(
            request,
            "Your message has been sent successfully."
        )

        return redirect("contact")

    return render(request, "pg/contact.html")


def register(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)

        if form.is_valid():
            form.save()

            messages.success(
                request,
                "Registration successful. You can now login."
            )

            return redirect("login")

    else:
        form = RegistrationForm()

    return render(request, "pg/register.html", {"form": form})


# LOGIN WITH OTP
def user_login(request):

    if request.method == "POST":

        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(
            request,
            username=username,
            password=password
        )

        if user is not None:

            # Generate 6 digit OTP
            otp = random.randint(100000, 999999)

            # Store OTP and username in session
            request.session["otp"] = str(otp)
            request.session["otp_user_id"] = user.id

            # Send OTP
            send_mail(
                "Sudarshan PG Login OTP",
                f"Your OTP for Sudarshan PG login is: {otp}",
                None,
                [user.email],
                fail_silently=False,
            )

            messages.success(
                request,
                "OTP has been generated. Check the Django terminal."
            )

            return redirect("verify_otp")

        messages.error(
            request,
            "Invalid username or password."
        )

    return render(request, "pg/login.html")


# OTP VERIFICATION
def verify_otp(request):

    if request.method == "POST":

        entered_otp = request.POST.get("otp")
        stored_otp = request.session.get("otp")
        user_id = request.session.get("otp_user_id")

        if stored_otp and entered_otp == stored_otp:

            from django.contrib.auth.models import User

            user = User.objects.get(id=user_id)

            login(request, user)

            # Remove OTP after successful verification
            request.session.pop("otp", None)
            request.session.pop("otp_user_id", None)

            messages.success(
                request,
                "Login successful."
            )

            return redirect("dashboard")

        else:

            messages.error(
                request,
                "Invalid OTP. Please try again."
            )

    return render(request, "pg/verify_otp.html")


def user_logout(request):
    logout(request)
    return redirect("home")


def dashboard(request):

    if not request.user.is_authenticated:
        return redirect("login")

    bookings = Booking.objects.filter(
        user=request.user
    ).order_by("-booking_date")

    complaints = Complaint.objects.filter(
        user=request.user
    ).order_by("-created_at")

    return render(
        request,
        "pg/dashboard.html",
        {
            "bookings": bookings,
            "complaints": complaints
        }
    )


def gallery(request):
    gallery_items = Gallery.objects.all()

    return render(
        request,
        "pg/gallery.html",
        {"gallery_items": gallery_items}
    )


def complaint(request):

    if not request.user.is_authenticated:
        return redirect("login")

    if request.method == "POST":

        form = ComplaintForm(request.POST)

        if form.is_valid():

            complaint = form.save(commit=False)
            complaint.user = request.user
            complaint.save()

            messages.success(
                request,
                "Complaint submitted successfully."
            )

            return redirect("dashboard")

    else:
        form = ComplaintForm()

    return render(
        request,
        "pg/complaint.html",
        {"form": form}
    )