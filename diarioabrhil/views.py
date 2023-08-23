from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.conf import settings
from .serializers import RegistroSerializer, UserSerializer
from django.contrib.auth.forms import UserCreationForm
from .forms import CustomUserCreationForm



# Create your views here.
from rest_framework import viewsets
from .models import Registro
from .serializers import RegistroSerializer

class RegistroViewSet(viewsets.ModelViewSet):
    queryset = Registro.objects.all()
    serializer_class = RegistroSerializer

class UserRegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        token, _ = Token.objects.get_or_create(user=user)

        # Enviar correo de bienvenida
        send_mail(
            'Bienvenido a Diario',
            f'Hola {user.username}, ¡bienvenido a Diario!',
            settings.EMAIL_HOST_USER,
            [user.email],
            fail_silently=False,
        )



@login_required
def create_entry(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        image = request.FILES.get('image')  # Obtén la imagen si se proporciona

        # Crea un nuevo registro
        nuevo_registro = Registro(usuario=request.user, titulo=title, contenido=content, imagen=image)
        nuevo_registro.save()

        return redirect('create_entry')  # Redirige nuevamente a la página de creación de entradas

    return render(request, 'create_entry.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('create_entry')  # Redirige a la página de creación de entradas
        else:
            return render(request, 'error_loggin.html')

    return render(request, 'home.html')

def user_register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Enviar correo de bienvenida
            send_mail(
                'Bienvenido a Diario',
                f'Hola {user.username}, ¡bienvenido a Diario!',
                settings.EMAIL_HOST_USER,
                [user.email],
                fail_silently=False,
            )
            # Iniciar sesión al usuario automáticamente
            login(request, user)
            return redirect('create_entry')  # Redirige a la página de creación de entradas

    else:
        form = UserCreationForm()
    
    return render(request, 'register.html', {'form': form})