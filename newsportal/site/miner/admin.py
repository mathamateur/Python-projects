from django.contrib import admin
from .models import News, Log


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = ("reporter_name", "title", "time")


@admin.register(Log)
class LogAdmin(admin.ModelAdmin):
    list_display = ("level_name", "message", "time")
