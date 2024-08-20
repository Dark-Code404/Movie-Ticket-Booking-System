from django.utils.dateformat import format
from django.contrib.auth.models import User
from django.db import models

class Cinemas(models.Model):
    cid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    role = models.CharField(max_length=30, default='Cinema Admin')
    phone = models.CharField(max_length=20)
    city = models.CharField(max_length=200)
    location = models.CharField(max_length=200)
    user = models.OneToOneField(User,null=True,on_delete=models.CASCADE)  

    def __str__(self):
        return self.name

class Actor(models.Model):
    name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    biography = models.TextField(null=True, blank=True)
    photo = models.ImageField(upload_to='actors/', null=True, blank=True)

    def __str__(self):
        return self.name
    

class Director(models.Model):
    did = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='director/', null=True)

    def __str__(self):
        return self.name



class Movies(models.Model):
    mid = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    trailer = models.URLField(max_length=300, default="null")
    release_date = models.CharField(max_length=20, default="null")
    description = models.TextField()
    poster = models.ImageField(upload_to='movies', default="")
    genre = models.CharField(max_length=50, default="Action | Comedy | Romance")
    duration = models.CharField(max_length=10, default="2hr 45min")
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    actors = models.ManyToManyField(Actor, related_name='movies', blank=True)
    director = models.ForeignKey(Director,on_delete=models.CASCADE,null=True,blank=True)
    upcoming=models.BooleanField(default=False)
    nowshowing=models.BooleanField(default=False)


    def __str__(self):
        return self.name

class ShowDate(models.Model):
    date = models.DateField(null=True, blank=True)  
    showdates=models.ForeignKey('Cinemas',on_delete=models.CASCADE,null=True) 

    def __str__(self):
        return format(self.date, 'Y-m-d') if self.date is not None else 'No date'

class ShowTime(models.Model):
    time = models.CharField(max_length=100, null=True)
    showtimes=models.ForeignKey('Cinemas',on_delete=models.CASCADE,null=True) 
    
    def __str__(self):
        return self.time

class Screening(models.Model):
    sid = models.AutoField(primary_key=True)
    cinema = models.ForeignKey(Cinemas, on_delete=models.CASCADE, related_name='cinema_show')
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, related_name='movie_show')
    available_date = models.ManyToManyField(ShowDate,)
    price = models.IntegerField()
    total_seats = models.IntegerField(default=100)
    available_seats = models.IntegerField(default=100)
    time = models.ManyToManyField(ShowTime)

    def __str__(self):
        date=','.join([format(date.date,'y-m-d') for date in self.available_date.all()])
        return f"{self.cinema.name} | {self.movie.name} | {date if date else ''}"

class Bookings(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    show_name = models.CharField(max_length=200, null=True)  
    showtime = models.ForeignKey(ShowTime, on_delete=models.CASCADE, null=True)
    user_seat = models.CharField(max_length=300, null=True)
    show_date = models.ForeignKey(ShowDate, on_delete=models.CASCADE, null=True)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    cinema_name = models.CharField(max_length=200, null=True)  
    cinema_location = models.CharField(max_length=200, null=True)  
    total_seat = models.CharField(max_length=200, null=True)
    is_visible = models.BooleanField(default=True)
    
    @property
    def user_seat_as_list(self):
        return self.user_seat.split(',')

    def __str__(self):
        if self.showtime:
            return f"{self.user.username} | {self.showtime}"
        return f"{self.user.username} | No ShowTime"
    




class Contact(models.Model):
    name=models.CharField(max_length=200)
    email=models.EmailField(max_length=250)
    subject=models.CharField(max_length=200)
    message=models.TextField()


    def __str__(self):
        return f"{self.name} | {self.message}"
    