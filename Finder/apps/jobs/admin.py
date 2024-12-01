from django.contrib import admin
from .models import Quotation, Review


# Register your models here.
admin.site.register(Quotation)
admin.site.register(Review)