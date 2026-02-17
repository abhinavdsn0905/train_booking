from django.shortcuts import render, redirect, get_object_or_404
from trains.models import Train
from django.conf import settings
from .models import Booking 
from django.core.mail import send_mail
from user.models import User

def booking_page(request):
    if not request.session.get("username"):
        return redirect("login")

    return render(request, "booking.html")


from datetime import date


def book_train(request, train_id):

    if not request.session.get("username"):
        return redirect("login")

    train = get_object_or_404(Train, id=train_id)

    if request.method == "POST":

        travel_date = request.POST.get("travel_date")
        passengers = int(request.POST.get("passengers"))

        # Prevent past date
        if date.fromisoformat(travel_date) < date.today():
            return render(request, "bookings.html", {
                "train": train,
                "error": "You cannot select a past date"
            })

        if train.available_seats < passengers:
            return render(request, "bookings.html", {
                "train": train,
                "error": "Not enough seats available"
            })

        details = ""
        for i in range(1, passengers + 1):
            name = request.POST.get(f"name_{i}")
            age = request.POST.get(f"age_{i}")
            gender = request.POST.get(f"gender_{i}")
            details += f"{name}, {age}, {gender}\n"

        total = passengers * train.price

        booking = Booking.objects.create(
            username=request.session.get("username"),
            train=train,
            travel_date=travel_date,
            passengers=passengers,
            passenger_details=details,
            total_price=total
        )

        train.available_seats -= passengers
        train.save()

        return redirect("booking_summary", booking_id=booking.id)

    return render(request, "bookings.html", {"train": train})

def my_bookings(request):

    if not request.session.get("username"):
        return redirect("login")

    bookings = Booking.objects.filter(
        username=request.session.get("username")
    )

    return render(request, "my_bookings.html", {
        "bookings": bookings
    })



def booking_summary(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)
    return render(request, "booking_summary.html", {"booking": booking})


def cancel_booking(request, booking_id):
    booking = get_object_or_404(Booking, id=booking_id)

    train = booking.train
    train.available_seats += booking.passengers
    train.save()

    booking.delete()

    return redirect("my_bookings")
