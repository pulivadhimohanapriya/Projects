from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("rooms/", views.rooms, name="rooms"),
    path("rooms/<int:room_id>/", views.room_detail, name="room_detail"),
    path("rooms/<int:room_id>/book/", views.booking, name="booking"),

    path("about/", views.about, name="about"),
    path("facilities/", views.facilities, name="facilities"),
    path("contact/", views.contact, name="contact"),
    path("gallery/", views.gallery, name="gallery"),

    path("register/", views.register, name="register"),
    path("login/", views.user_login, name="login"),
    path("verify-otp/", views.verify_otp, name="verify_otp"),
    path("logout/", views.user_logout, name="logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("complaint/", views.complaint, name="complaint"),
]