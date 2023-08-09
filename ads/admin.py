from django.contrib import admin
from .models import Ad, Comment, Fav, Car, Owner, Make


class AdAdmin(admin.ModelAdmin):
    # excluding some fields for admin
    exclude = ('picture', 'content_type')
    # Adding search field in the admin panel
    search_fields = ('text',)
    # Adding the ability to filter by date
    list_filter = ('created_at',)


# registering models
admin.site.register(Ad, AdAdmin),
admin.site.register(Comment)
admin.site.register(Car)
admin.site.register(Fav)
admin.site.register(Owner)
admin.site.register(Make)
