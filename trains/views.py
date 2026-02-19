from django.shortcuts import render

# Create your views here.
from .models import Train
def train_list(request):

    trains = Train.objects.all()

    source = request.GET.get("source")
    destination = request.GET.get("destination")
    min_price = request.GET.get("min_price")
    max_price = request.GET.get("max_price")
    sort = request.GET.get("sort")

    if source:
        trains = trains.filter(source__icontains=source)

    if destination:
        trains = trains.filter(destination__icontains=destination)

    if min_price:
        trains = trains.filter(price__gte=min_price)

    if max_price:
        trains = trains.filter(price__lte=max_price)

    if sort == "price_low":
        trains = trains.order_by("price")

    if sort == "price_high":
        trains = trains.order_by("-price")

    if sort == "departure":
        trains = trains.order_by("departure_time")

    return render(request, "train_list.html", {
        "trains": trains
    })