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

@login_required(login_url='/auth/login/')
@user_passes_test(is_admin, login_url='/')  
def admin_dashboard(request):
    # Retrieve all bookings with related information for efficient queries
    bookings = Bookings.objects.all().select_related('showtime', 'show_date', 'user')

    # Calculate total income from bookings
    total_income = sum(
        booking.total_price for booking in bookings
    )

    # Prepare context for the template
    context = {
        'bookings': bookings,
        'total_income': total_income,
    }

    # Render the template with booking data
    return render(request, 'admin_dashboard.html', context)

def home(request):
  
    cinemas = Cinemas.objects.all()

    # Get the search query from the GET parameters
    search_query = request.GET.get('search', '')

    # Filter movies based on their status and search query
    if search_query:
        now_showing_movies = Movies.objects.filter(nowshowing=True, name__icontains=search_query)
        upcoming_movies = Movies.objects.filter(upcoming=True, name__icontains=search_query)
    else:
        now_showing_movies = Movies.objects.filter(nowshowing=True)
        upcoming_movies = Movies.objects.filter(upcoming=True)

    # Pass both sets of movies and the search query to the template
    context = {
        'cinemas': cinemas,
        'now_showing_movies': now_showing_movies,
        'upcoming_movies': upcoming_movies,
        'search_query': search_query,
    }

    return render(request, 'home.html', context)


@login_required(login_url='/auth/login/')
def showtime(request, mid):
    movie = get_object_or_404(Movies, pk=mid)
    shows = Screening.objects.filter(movie=movie)
    
    is_upcoming = movie.upcoming

    available_dates = set()
    if not is_upcoming:
        for show in shows:
            available_dates.update(show.available_date.all())

        selected_date = request.GET.get('date')

        if selected_date:
            shows = shows.filter(available_date__date=selected_date)

        showtime_seats = {}
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

    # Assuming you want to pass the cinema name of the first showtime
    cinema_name = shows.first().cinema.name if shows.exists() else ''

    return render(request, 'showtime.html', {
        'movie': movie,
        'available_dates': sorted(available_dates, key=lambda d: d.date),
        'selected_date': selected_date,
        'shows': shows,
        'showtime_seats': showtime_seats,
        'is_upcoming': is_upcoming,
        'cinema_name': cinema_name,  
    })



@login_required(login_url='/auth/login/')
def book_show(request):
    if request.method == 'POST':
        showtime_id = request.POST.get('showtime_id')
        show_date_str = request.POST.get('show_date')
        show_name = request.POST.get('show_name')
        

        if not showtime_id or not showtime_id.isdigit() or not show_date_str:
            messages.error(request, "Invalid showtime ID or date.")
            return redirect('home')

        showtime_id = int(showtime_id)
        showtime = get_object_or_404(ShowTime, pk=showtime_id)
        user = request.user

        shows_details = Screening.objects.filter(time=showtime).first()
        if not shows_details:
            messages.error(request, "Show details not found.")
            return redirect('home')

        try:
            show_date_obj = datetime.strptime(show_date_str, '%Y-%m-%d').date()
        except ValueError:
            messages.error(request, "Invalid date format.")
            return redirect('home')

        show_date, created = ShowDate.objects.get_or_create(date=show_date_obj)

        selected_seats = request.POST.getlist('seats')

        existing_bookings = Bookings.objects.filter(showtime=showtime, show_date=show_date)
        already_booked_seats = []
        for booking in existing_bookings:
            already_booked_seats.extend(booking.user_seat_as_list)

        if any(seat in already_booked_seats for seat in selected_seats):
            messages.error(request, "Some of the selected seats are already booked.")
            return redirect('showtime', mid=shows_details.movie.mid)

        total_price = shows_details.price * len(selected_seats)
        
        # Create the booking and save the show name
        booking = Bookings.objects.create(
            user=user,
            showtime=showtime,
            show_date=show_date,
            user_seat=','.join(selected_seats),
            total_price=total_price,
            cinema_name=shows_details.cinema.name,
            cinema_location=shows_details.cinema.city + "," + shows_details.cinema.location,
            total_seat=len(selected_seats),
            show_name=show_name  
        )

        messages.success(request, f"Your seats have been booked successfully. Total price: ${total_price:.2f}")

        return redirect('my_ticket')

    return redirect('home')





@login_required(login_url='/auth/login/')
def download_ticket(request, booking_id):
    booking = get_object_or_404(Bookings, pk=booking_id, user=request.user)

    # Load the template for the ticket
    template = get_template('ticket_template.html')
    context = {'booking': booking}
    html = template.render(context)

    # Generate the PDF
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="ticket_{booking.id}.pdf"'
    pisa_status = pisa.CreatePDF(html, dest=response)

    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')

    return response


@login_required(login_url='/auth/login/')
def my_tickets(request):
    # Get all tickets booked by the user
    shows_details_prefetch = Prefetch(
        'showtime__shows_details_set', 
        queryset=Screening.objects.select_related('cinema')
    )

    bookings = Bookings.objects.filter(user=request.user).prefetch_related(shows_details_prefetch)

    context = {
        'bookings': bookings,
    }
    return render(request, 'my_ticket.html', context)









def contact(request):
    return render(request, 'contact.html')
