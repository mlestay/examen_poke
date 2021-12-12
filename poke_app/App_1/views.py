from django.shortcuts import render, redirect, HttpResponse, get_object_or_404
from django.contrib import messages
import re
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.template import RequestContext, context
from django.http import HttpResponseRedirect
from django.forms import ModelForm
from django.contrib import auth
from django.db.models import Count
from datetime import datetime, time, timezone
from time import gmtime, strftime 
from App_1.models import User, Poke



EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

#pagina de inicio
def index(request):
    if 'login' not in request.session:
        request.session['login'] = False
    
    if 'u_id' not in request.session:
        request.session['u_id'] = 0
    return render(request,'index.html')

#registrarse
def registro(request):    
    error = False

    if len(request.POST['name'])< 5:
        messages.error(request,'Tu nombre debe contener al menos 5 carácteres.', extra_tags = 'fn_error' )
        error = True

    if len(request.POST['alias'])< 4:
        messages.error(request,'Tu alias debe tener al menos 4 carácteres.', extra_tags = 'ln_error')
        error = True

    if request.POST['password'] != request.POST['confirm_password']:
        messages.error(request,'Las contraseñas deben coincidir', extra_tags = 'pw_error')
        error = True

    if len(request.POST['password']) < 8 :
        messages.error(request,'Tu contraseña debe tener 8 carácteres como mínimo', extra_tags = 'pw_error')
        error = True

    if error == True:
        return redirect(request,'/pokes')

    elif error == False:
        new_User = User.objects.create(name = request.POST['name'], alias = request.POST['alias'],email=request.POST['email'], password=request.POST['password'], dob=request.POST['date_of_birthday'])
        print(new_User)
        request.session['user_id'] = new_User.id
        messages.success(request, 'Ya cuentas con una cuenta, ahora debes iniciar sesión', extra_tags = 'registered')
        
        return redirect(request,'/index')

#loggearse
def login(request):
    if request.method == 'POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            acceso = authenticate(username=usuario, password=clave)
            return HttpResponseRedirect('/pokes')
    else:
        formulario = AuthenticationForm()
    return HttpResponseRedirect('/index')


#mostrar el perfil y los me gusta
def perfil(request,user_id):
    if request.method == 'GET':
        user = User.objects.filter(id=user_id)
        if user:
            user = user[0]
            context = {
                'info_perfil': user
            }
            return render(request, '/pokes.html', context)
        return redirect('/pokes')

#mostrar me gusta
def me_gusta(request):
    print('Listado de tus me gusta')
    if request.session['login'] == True:
        User_1 = User.objects.get(id = request.session['u_id'])
        conteo_megusta = Poke.objects.get(poke_list=User_1)
        context = {
            'usuarios': User.objects.all(),
            'User': User_1,
            'conteo_mgusta': conteo_megusta,
        }
        print(conteo_megusta)
        return render(request,'poke.html', context)
    else:
        print("debes iniciar sesión")
        context = {
            'usuarios': User.objects.all(),
        }
        return render(request, 'index.html', context)


#agregar me gusta
def add_poke (request,user_id):
    if request.session['login'] == True:
        alias = User.objects.get(id = request.session['alias'])
        if request.method == 'GET':
            Poke.poke_list.add([Poke.Poke_it(alias)])
            print(Poke.poke_list.count())
            context={
                'usuario': alias,

            }
            return render(request,'/pokes.html',context)
    else:
        print("debes iniciar sesion para dar me gusta")
        return redirect(render, '/index')

def lista_usuarios(request):
    lista_usuarios = User.objects.all(alias=['alias'])
    if request.session['login'] == True:
        context = {
            'lista_usuarios' : lista_usuarios,
        }
        print(lista_usuarios)
    return render(request, '/pokes.html', context)

#salir de sesion
def logout(request):
    if request.session['login'] == True:
        logout(request)
    return redirect('/index.html')