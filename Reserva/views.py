from django.shortcuts import render, redirect
from django.contrib.auth.models import AnonymousUser, User
from django.contrib.auth import login,logout, authenticate
from django.shortcuts import HttpResponse, get_object_or_404
from Reserva.models import Cancha, Persona, Horario, Reserva, Pago
from django.views.generic import TemplateView
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from Reserva.forms import RegistroForm
#Nuevo soporte rest 

from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework import status
from Reserva.serializer import (
    PersonaSerializer, CanchaSerializer, HorarioSerializer, 
    ReservaSerializer, PagoSerializer, UserSerializer,ReservaDetailSerializer, PagoDetailSerializer
)
from rest_framework_simplejwt.tokens import RefreshToken
# Create your views here.

def get_info_cancha_by_id(request, id_cancha):
    cancha = Cancha.objects.get(id= id_cancha)
    horarios= Horario.objects.filter(cancha=id_cancha)
  
    return render(request=request, template_name='cancha.html', context={'cancha':cancha, 'horarios': horarios})

def get_persona_by_id(id_persona):
    persona = Persona.objects.get(id= id_persona)
    resultado_layout = f"<h3>Nombre: {persona.nombre} Apellido: {persona.apellido} Telefono: {persona.telefono}</h3>"
    return HttpResponse(resultado_layout)

class MainView(TemplateView):
    template_name="main.html"

def tubpla_return(valor):
 return (valor.id, valor.nombre)
def getListadoCanchas(request):
    canchas = Cancha.objects.all()
    list_resultado = list(map(tubpla_return, canchas))
    return render(request,"canchas.html", {'listado':list_resultado})
    

def registro_request(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("landing")
        messages.error(request, form.errors)
    form = RegistroForm()   
    return render(request=request, template_name='registro.html', context={'registro_form':form})

def login_request(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')

            user = authenticate(username= username, password= password)
            if user is not None:
                login(request, user)
                return redirect("landing")
            messages.error(request, 'Error al auntenticarse')
        messages.error(request, form.errors)
 
    form = AuthenticationForm()
    return render(request=request, template_name='login.html', context={'login_form':form})


def logout_request(request):
    logout(request)
    messages.info(request, "Has cerrrado sesion")
    return redirect('login')

def reservarCancha(request, id_horario):
    if request.method=='POST':
        user_id= request.user.id
        print(user_id)
        persona= Persona.objects.get(user_id= user_id)
        horario= Horario.objects.get(id= id_horario)

        new_reserva = Reserva(horario=horario, persona= persona)
        new_reserva.save()

        messages.info(request,'Se ha reservado la cancha')

        return redirect(f'/getInfoCanchaById/{horario.cancha.id}')
    

#Refactorizado para soporte REST
@api_view(['GET'])
def get_info_cancha_by_id(id_cancha):
    cancha = get_object_or_404(Cancha, id=id_cancha)
    horarios = Horario.objects.filter(cancha=id_cancha)

    reservada = False
    reserva_persona = None
    for horario in horarios:
        reserva = Reserva.objects.filter(horario=horario).first()
        if reserva:
            reservada = True
            reserva_persona = f"{reserva.persona.nombre} {reserva.persona.apellido}"
            break
    cancha_serializer = CanchaSerializer(cancha)
    horarios_serializer = HorarioSerializer(horarios, many=True)
    return Response({
        'cancha': cancha_serializer.data,
        'horarios': horarios_serializer.data,
          'reservada': reservada,
        'reserva_persona': reserva_persona
    })
@api_view(['GET'])
def get_persona_by_id(id_persona):
    persona = get_object_or_404(Persona, id=id_persona)
    serializer = PersonaSerializer(persona)
    return Response(serializer.data)

@api_view(['GET'])
def get_listado_canchas():
    canchas = Cancha.objects.all()
    serializer = CanchaSerializer(canchas, many=True)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([AllowAny])
def registrar_usuario(request):
    data = request.data
    user = User.objects.create_user(
        username=data['username'], password=data['password']
    )
    persona = Persona.objects.create(
        user=user, nombre=data['nombre'], apellido=data['apellido'],
        cedula=data['cedula'], telefono=data['telefono']
    )
    serializer = UserSerializer(user)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def login_usuario(request):
    from django.contrib.auth import authenticate
    data = request.data
    user = authenticate(username=data['username'], password=data['password'])
    print('Es user',user)
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

@api_view(['POST'])
def reservar_cancha(request, id_horario):
    user_id = request.user.id
    persona = get_object_or_404(Persona, user_id=user_id)
    horario = get_object_or_404(Horario, id=id_horario)
    new_reserva = Reserva.objects.create(horario=horario, persona=persona)
    serializer = ReservaSerializer(new_reserva)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def registrar_pago(request):
    user = request.user
    data = request.data

    try:
        reserva = Reserva.objects.get(id=data['reserva_id'])
        if reserva.persona.user != user:
            return Response({'detail': 'Unauthorized'}, status=status.HTTP_401_UNAUTHORIZED)

        pago = Pago.objects.create(
            reserva=reserva,
            total=data['total']
        )

        serializer = PagoSerializer(pago)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    except Reserva.DoesNotExist:
        return Response({'detail': 'Reserva not found'}, status=status.HTTP_404_NOT_FOUND)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def historial_pagos(request):
    user = request.user
    print(user)
    persona = user.persona
    reservas = Reserva.objects.filter(persona=persona)
    pagos = Pago.objects.filter(reserva__in=reservas)
    serializer = PagoDetailSerializer(pagos, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_reservations(request):
    user = request.user
    if isinstance(user, AnonymousUser):
        return Response({'detail': 'Authentication credentials were not provided.'}, status=401)
    
    try:
        persona = Persona.objects.get(user=user)
        reservas = Reserva.objects.filter(persona=persona)
        serializer = ReservaDetailSerializer(reservas, many=True)
        return Response(serializer.data)
    except Persona.DoesNotExist:
        return Response({'detail': 'No persona associated with this user.'}, status=404)
