from django.contrib import admin

from MT_main.models import *


class Movies_actors_filter(admin.ModelAdmin):
    
  
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        
       
        form.base_fields['actors'].queryset = Actor.objects.filter(movies__isnull=True)
        return form


admin.site.register(Cinemas)
admin.site.register(Movies,Movies_actors_filter)
admin.site.register(Screening)
admin.site.register(Bookings)
admin.site.register(ShowTime)
admin.site.register(Actor)
admin.site.register(ShowDate)
admin.site.register(Director)
admin.site.register(Contact)

