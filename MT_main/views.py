from django.shortcuts import get_object_or_404, redirect, render
from MT_main.models import *
from django.contrib.auth.decorators import *
from django.contrib import messages
from datetime import datetime
from django.template.loader import get_template
from django.http import HttpResponse
from xhtml2pdf import pisa
from django.db.models import Prefetch


def is_admin(user):
    return user.is_superuser


@login_required(login_url="/auth/login/")
@user_passes_test(is_admin, login_url="/")
def admin_dashboard(request):

    bookings = Bookings.objects.all().select_related("showtime", "show_date", "user")

    totalIncome = sum(booking.total_price for booking in bookings)

    context = {
        "bookings": bookings,
        "totalIncome": totalIncome,
    }

    return render(request, "admin_dashboard.html", context)


def home(request):
    cinemas = Cinemas.objects.all()

    search_query = request.GET.get("search", "")

    if search_query:
        now_showing = Screening.objects.filter(
            nowshowing=True, movie__name__icontains=search_query
        )
        upcoming_movies = Screening.objects.filter(
            upcoming=True, movie__name__icontains=search_query
        )
    else:
        now_showing = Screening.objects.filter(nowshowing=True)
        upcoming_movies = Screening.objects.filter(upcoming=True)

    context = {
        "cinemas": cinemas,
        "now_showing": now_showing,
        "upcoming_movies": upcoming_movies,
        "search_query": search_query,
    }

    return render(request, "home.html", context)

def showtime(request, mid):
    movie = get_object_or_404(Movies, pk=mid)
    shows = Screening.objects.filter(movie=movie)

   
    is_upcoming = shows.filter(upcoming=True).exists()

    seats_row = ["A","B","C","D"]
    seats_column = ["1", "2", "3", "4", "5","6","7","8","9","10"]
    selected_date = request.GET.get("date")
    showtime_id = request.GET.get("showtime_id")

    available_dates = set()
    showtime_seats = {}

    if not is_upcoming:
        for show in shows:
            available_dates.update(show.available_date.all())

        if selected_date:
            try:
                selected_date_obj = datetime.strptime(selected_date, "%Y-%m-%d").date()
                shows = shows.filter(available_date__date=selected_date_obj)

            except ValueError:
                messages.error(request, "Invalid date format")
                return redirect("home")

        if showtime_id:
            selected_showtime = get_object_or_404(ShowTime, pk=showtime_id)
            bookings = Bookings.objects.filter(showtime=selected_showtime)
            booked_seats = []
            for booking in bookings:
                booked_seats.extend(booking.user_seat_as_list)
            showtime_seats[showtime_id] = booked_seats

        else:
            for show in shows:
                for slot in show.time.all():
                    bookings = Bookings.objects.filter(showtime=slot)
                    booked_seats = []
                    for booking in bookings:
                        booked_seats.extend(booking.user_seat_as_list)
                    showtime_seats[slot.id] = booked_seats
    else:
        available_dates = []
        selected_date = None
        showtime_seats = {}

    cinema_name = shows.first().cinema.name if shows.exists() else ""

    print(f"showtime seats : {showtime_seats} ")
    print(f"showtime id : {showtime_id} ")

    return render(request,"showtime.html",
        {
            "movie": movie,
            "available_dates": sorted(available_dates, key=lambda d: d.date),
            "selected_date": selected_date,
            "shows": shows,
            "showtime_seats": showtime_seats,
            "showtime_id": showtime_id,
            "is_upcoming": is_upcoming,
            "cinema_name": cinema_name,
            "seats_row": seats_row,
            "seats_column": seats_column,
        },
    )



@login_required(login_url="/auth/login/")
def book_show(request):
    if request.method == "POST":
        showtime_id = request.POST.get("showtime_id")
        show_date_str = request.POST.get("show_date")
        show_name = request.POST.get("show_name")

        movie_id = request.POST.get("movie_id")

        movies = get_object_or_404(Movies, pk=movie_id)

        

        if not showtime_id or not showtime_id.isdigit() or not show_date_str:
            messages.error(request, "Invalid showtime ID or date.")
            return redirect("home")

        showtime_id = int(showtime_id)
        showtime = get_object_or_404(ShowTime, pk=showtime_id)
        user = request.user
        screen = Screening.objects.filter(movie=movies, time=showtime_id).first()

        shows_details = Screening.objects.filter(time=showtime).first()
        if not shows_details:
            messages.error(request, "Show details not found.")
            return redirect("home")

        try:
            show_date_obj = datetime.strptime(show_date_str, "%Y-%m-%d").date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect("home")

        show_date, created = ShowDate.objects.get_or_create(date=show_date_obj)

        selected_seats = request.POST.getlist("seats")

        existing_bookings = Bookings.objects.filter(
            showtime=showtime, show_date=show_date
        )
        already_booked_seats = []
        for booking in existing_bookings:
            already_booked_seats.extend(booking.user_seat_as_list)

        if any(seat in already_booked_seats for seat in selected_seats):
            messages.error(request, "Some of the selected seats are already booked.")
            return redirect("showtime", mid=shows_details.movie.mid)

        total_price = shows_details.price * len(selected_seats)

        if shows_details.available_seats < len(selected_seats):
            messages.error(request, "Not enough seat")
            return redirect("showtime", mid=shows_details.movie.mid)

        shows_details.available_seats -= len(selected_seats)
        shows_details.save()

        booking = Bookings.objects.create(
            user=user,
            showtime=showtime,
            show_date=show_date,
            user_seat=",".join(selected_seats),
            total_price=total_price,
            cinema_name=shows_details.cinema.name,
            cinema_location=shows_details.cinema.city
            + ","
            + shows_details.cinema.location,
            total_seat=len(selected_seats),
            show_name=show_name,
            screen=screen,
        )

        messages.success(
            request,
            f"Your seats have been booked successfully. Total price: ${total_price:.2f}",
        )

        return redirect("my_ticket")

    return redirect("home")


@login_required(login_url="/auth/login/")
def download_ticket(request, booking_id):
    booking = get_object_or_404(Bookings, pk=booking_id, user=request.user)

    template = get_template("ticket_template.html")
    context = {"booking": booking}
    html = template.render(context)

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = f'attachment; filename="ticket_{booking.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse("We had some errors <pre>" + html + "</pre>")

    return response


@login_required(login_url="/auth/login/")
def my_tickets(request):
    if request.method == "POST" and "delete_ticket" in request.POST:
        booking_id = request.POST.get("booking_id")
        booking = get_object_or_404(Bookings, pk=booking_id, user=request.user)
        booking.is_visible = False
        booking.save()
        messages.success(
            request, "Your booking has been successfully removed from your view."
        )
        return redirect("my_ticket")

    bookings = (
        Bookings.objects.filter(user=request.user, is_visible=True)
        .select_related("showtime", "show_date")
        .prefetch_related(Prefetch("showtime__screening_set"))
    )

    context = {
        "bookings": bookings,
    }
    return render(request, "my_ticket.html", context)


def contact(request):

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")
        try:
            Contact.objects.create(
                name=name, email=email, subject=subject, message=message
            )
            messages.error(request, f"Contact submitted successfully  ")

        except Exception as e:
            messages.error(request, f"Contact not submitted successfully : {e}")

    return render(request, "contact.html")
