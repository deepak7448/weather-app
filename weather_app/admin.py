from django.contrib import admin
from .models import City, forecast, feedback
# Register your models here.
admin.site.register(City)
admin.site.register(forecast)
admin.site.register(feedback)
    