from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from .forms import tareaForma
from .models import tarea
from django.utils import timezone
from django.contrib.auth.decorators import login_required
# Create your views here.

def home(request):
    return render(request, "home.html")


def signup(request):
    if request.method == "GET":
        return render(request, "signup.html", {"form": UserCreationForm})
        # print('enviando datos')
    else:
        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    username=request.POST["username"],
                    password=request.POST["password1"],
                )
                user.save()
                login(request, user)
                return redirect("tarea1")
            except IntegrityError:
                # return HttpResponse('usuario creado satisfatoriamente')
                return render(request, "signup.html", {"form": UserCreationForm, 'error': 'usuario ya existe'})
        #return HttpResponse("las claves no son correctas")
        return render(request, "signup.html", {"form": UserCreationForm, 'error': 'las claves no son correctas'})
        # print(request.POST)
        # print('recibiendo datos')

@login_required
def tareac(request):
    tarea2 = tarea.objects.filter(user = request.user, fechaCompleta__isnull = True)
    return render(request, 'tarea.html', {'tarea': tarea2})

@login_required
def tareaCompleta(request):
    tarea2 = tarea.objects.filter(user = request.user, fechaCompleta__isnull = False).order_by('-fechaCompleta')
    return render(request, 'tarea.html', {'tarea': tarea2})

@login_required
def tareaDetallada(request, tarean_Id):
    if request.method == 'GET':
        tarea3 = get_object_or_404(tarea,  pk=tarean_Id, user = request.user)
        form = tareaForma(instance= tarea3)
        return render(request, 'tareaDeta.html', {'tarea': tarea3, 'form': form})
    else:
        try:
            tarea3 = get_object_or_404(tarea, pk=tarean_Id, user = request.user)
            form = tareaForma(request.POST, instance= tarea3)
            form.save()
            return redirect('tarea1')
        except ValueError:
            return render(request, 'tareaDeta.html', {'tarea': tarea3, 'form': form, 'error': 'error al actualizar'})
            
    #tarea3 = 'hola'

@login_required
def completarTarea(request, tarean_Id):
    tarea4 = get_object_or_404(tarea, pk= tarean_Id, user = request.user)
    if request.method == 'POST':
        tarea4.fechaCompleta =  timezone.now()
        tarea4.save()
        return redirect('tarea1')  

@login_required
def eliminarTarea(request, tarean_Id):
    tarea4 = get_object_or_404(tarea, pk= tarean_Id, user = request.user)
    if request.method == 'POST':
        tarea4.delete()
        return redirect('tarea1') 

@login_required
def signout(request):
    logout(request)
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        user = authenticate(request, username = request.POST['username'], password = request.POST['password'] )
        if user is None:
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'usuario y clave invalidad'})
        else:
            login(request, user)
            return redirect('tarea1')
        
@login_required
def creat_tarea(request):
    if request.method == 'GET':
        return render(request, 'creat_tarea.html', {'form': tareaForma})
    else:
        try:
            form = tareaForma(request.POST)
            nuevaTarea = form.save(commit=False)
            nuevaTarea.user = request.user
            nuevaTarea.save()
            return redirect('tarea1')
        except ValueError:
            return render(request, 'creat_tarea.html', {'form': tareaForma, 'error': 'datos no validos'})
        
            