from django.contrib import admin
from .models import Job, Quotation, Review


# Register your models here.
admin.site.register(Job)
admin.site.register(Quotation)
admin.site.register(Review)