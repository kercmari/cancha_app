from rest_framework import serializers
from .models import Persona, Cancha, Horario, Reserva, Pago
from django.contrib.auth.models import User

class PersonaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Persona
        fields = '__all__'

class CanchaSerializer(serializers.ModelSerializer):
    reservada = serializers.SerializerMethodField()
    reserva_id = serializers.SerializerMethodField()
    horario_inicio = serializers.SerializerMethodField()
    horario_fin = serializers.SerializerMethodField()

    class Meta:
        model = Cancha
        fields = ['id', 'nombre', 'descripcion', 'costo_por_hora', 'reservada', 'reserva_id','horario_inicio', 'horario_fin']

    def get_reservada(self, obj):
        horarios = Horario.objects.filter(cancha=obj)
        for horario in horarios:
            if Reserva.objects.filter(horario=horario).exists():
                return True
        return False

    def get_reserva_id(self, obj):
        horarios = Horario.objects.filter(cancha=obj)
        for horario in horarios:
            reserva = Reserva.objects.filter(horario=horario).first()
            if reserva:
                return reserva.id
        return None
    def get_horario_inicio(self, obj):
        horario = Horario.objects.filter(cancha=obj).order_by('hora_inicio').first()
        if horario:
            return horario.hora_inicio
        return None

    def get_horario_fin(self, obj):
        horario = Horario.objects.filter(cancha=obj).order_by('-hora_fin').first()
        if horario:
            return horario.hora_fin
        return None

class HorarioSerializer(serializers.ModelSerializer):
    class Meta:
        model = Horario
        fields = '__all__'

class ReservaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reserva
        fields = '__all__'

class PagoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Pago
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']
class ReservaDetailSerializer(serializers.ModelSerializer):
    cancha_nombre = serializers.CharField(source='horario.cancha.nombre', read_only=True)
    horario_inicio = serializers.DateTimeField(source='horario.hora_inicio', read_only=True)
    horario_fin = serializers.DateTimeField(source='horario.hora_fin', read_only=True)
    costo_por_hora = serializers.FloatField(source='horario.cancha.costo_por_hora', read_only=True)

    class Meta:
        model = Reserva
        fields = ['id', 'cancha_nombre', 'horario_inicio', 'horario_fin', 'costo_por_hora']

class PagoDetailSerializer(serializers.ModelSerializer):
    cancha_nombre = serializers.CharField(source='reserva.horario.cancha.nombre', read_only=True)
    horario_inicio = serializers.DateTimeField(source='reserva.horario.hora_inicio', read_only=True)
    horario_fin = serializers.DateTimeField(source='reserva.horario.hora_fin', read_only=True)
    persona_nombre = serializers.CharField(source='reserva.persona.nombre', read_only=True)
    persona_apellido = serializers.CharField(source='reserva.persona.apellido', read_only=True)

    class Meta:
        model = Pago
        fields = ['id', 'fecha_creacion', 'total', 'cancha_nombre', 'horario_inicio', 'horario_fin', 'persona_nombre', 'persona_apellido']