from django.db import models
from django.contrib import admin


# Create your models here.
class News(models.Model):
    reporter_name = models.CharField(max_length=50)
    time = models.DateTimeField()
    title = models.CharField(max_length=255, default='')
    text = models.TextField(default='')
    main_news = models.BooleanField(default=False)
    importance = models.FloatField(default=0)

    class Meta:
        ordering = ['-main_news', '-importance']
        verbose_name = ('Новость')
        verbose_name_plural = ('Новости')

    def __str__(self):
        return self.reporter_name


class Log(models.Model):
    level_name = models.CharField(max_length=50)
    message = models.TextField()
    time = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = ('Лог')
        verbose_name_plural = ('Логи')

    def __str__(self):
        return self.level_name
