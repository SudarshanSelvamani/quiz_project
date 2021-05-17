from django.contrib import admin
from .models import Result, TempResultToStoreBetweenRequests
# Register your models here.

admin.site.register(Result)
admin.site.register(TempResultToStoreBetweenRequests)


