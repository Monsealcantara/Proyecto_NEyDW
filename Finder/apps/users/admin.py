from django.contrib import admin
from .models import User, Service, Keyword, Worker, WorkerService

# Registro de los modelos en el administrador de Django
admin.site.register(User)
admin.site.register(Service)
admin.site.register(Keyword)
admin.site.register(Worker)
admin.site.register(WorkerService)
