from django.contrib import admin
from .models import Persona, Cancha, Horario, Reserva, Pago
# Register your models here.

admin.site.register(Persona)
admin.site.register(Cancha)
admin.site.register(Horario)
admin.site.register(Reserva)
admin.site.register(Pago)
