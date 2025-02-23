from django.contrib import admin
from .models import *
from django.utils.html import format_html
from .models import Ticket


admin.site.register(Status)
admin.site.register(CustomUser)
admin.site.register(Categories)

@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = ('title', 'creator', 'created_at', 'display_photo')

    def display_photo(self, obj):
        if obj.photo:
            return format_html('<img src="{}" width="100" height="100" />', obj.photo.url)
        return "Нет фото"

    display_photo.short_description = 'Фото'