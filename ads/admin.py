from django.contrib import admin
from .models import Ad, Comment, Fav, Car, Owner, Make


class AdAdmin(admin.ModelAdmin):
    exclude = ('picture', 'content_type')
    # Добавляем интерфейс для поиска по тексту постов
    search_fields = ('text',)
    # Добавляем возможность фильтрации по дате
    list_filter = ('created_at',)


admin.site.register(Ad, AdAdmin),
admin.site.register(Comment)
admin.site.register(Car)
admin.site.register(Fav)
admin.site.register(Owner)
admin.site.register(Make)
