from django.contrib import admin
from .models import GetUrlModel, StoreURLDetailsModel
# Register your models here.

admin.site.register(GetUrlModel)
admin.site.register(StoreURLDetailsModel)