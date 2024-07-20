from django.urls import path
from .views import (
    get_info_cancha_by_id, get_persona_by_id, get_listado_canchas, 
    registrar_usuario, login_usuario, reservar_cancha, registrar_pago, historial_pagos,get_user_reservations
)

urlpatterns = [
    path('canchas/<int:id_cancha>/', get_info_cancha_by_id, name='get_info_cancha_by_id'),
    path('personas/<int:id_persona>/', get_persona_by_id, name='get_persona_by_id'),
    path('canchas/', get_listado_canchas, name='get_listado_canchas'),
    path('registrar/', registrar_usuario, name='registrar_usuario'),
    path('usuarios/login/', login_usuario, name='login_usuario'),
    path('reservas/<int:id_horario>/', reservar_cancha, name='reservar_cancha'),
    path('pagos/registrar/', registrar_pago, name='registrar_pago'),
    path('pagos/historial/', historial_pagos, name='historial_pagos'),
    path('reservas/mis-reservas/', get_user_reservations, name='get_user_reservations'),

]
