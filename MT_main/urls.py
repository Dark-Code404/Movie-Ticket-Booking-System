


from django.contrib import admin
from django.urls import include, path
from MT_main import views


urlpatterns = [
   
    path('', views.home, name='home'),
    path('contact/', views.contact, name='contact'),
    path('showtime/<int:mid>/', views.showtime, name='showtime'),
    path('book_show/', views.book_show, name='book_show'),
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
   path('my_ticket/', views.my_tickets, name='my_ticket'),
    path('download-ticket/<int:booking_id>/', views.download_ticket, name='download_ticket'),
    
]
