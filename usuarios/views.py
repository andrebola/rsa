
from django.shortcuts import render_to_response
from django.template import RequestContext
from comunes.forms import PaisesForm
from usuarios.models import Interesado
from usuarios.forms import InteresadoForm,RegisterForm,RelacionInteresadosForm
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from proyectos.models import Proyecto
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth import authenticate, login

# Primer paso del registo de un usuario
def registro_interesado_1(request):

    if request.method == 'POST':
        form_int=RegisterForm(request.POST)
        if form_int.is_valid():
            user=form_int.save()
            return HttpResponseRedirect("paso2/"+str(user.id)+"/")
        else:
            return HttpResponse(form_int.errors)
    else:
        return HttpResponse('ERROR')


# Segundo paso del registo de un usuario
def paso2(request,user_id):
    
    try:
        user=User.objects.get(id=user_id)
        interesado=Interesado.objects.filter(user=user)[0]
        interesado_form = InteresadoForm(instance=interesado)   
    except:
        return HttpResponse(interesado_form)
    
    if request.method =="POST":
        interesado_form = InteresadoForm(request.POST,request.FILES,instance=interesado) 
        if interesado_form.is_valid():
            interesado=interesado_form.save()
            interesado.save()
            interesado.user.is_active=True
            interesado.user.save()
            interesado.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request, interesado.user)
            return HttpResponseRedirect(reverse("proyectos.views.lista_proyectos",args=(2,)))
            
        
        else:
            return HttpResponse(interesado_form.errors)
        
    else:
        
        return render_to_response('usuarios/registro_paso2.html', {'interesado_form':interesado_form,'user':user},context_instance=RequestContext(request))
    return HttpResponse('Error en paso 2')

# Unirse a una discucion
@login_required
def participar(request,slug):
    try:
        proy = Proyecto.objects.get(slug=slug)
        if not request.user.interesado.proyectos_interes.filter(id=proy.id):
            if request.method == 'POST':
                form=RelacionInteresadosForm(proy,request.POST )
                if form.is_valid():
                    rela=form.save(commit=False)
                    rela.proyecto=proy
                    rela.interesado=request.user.interesado
                    rela.save()
                    return HttpResponseRedirect(reverse("discucion.views.discucion_gral",args=(slug,)))
            else:
                form=RelacionInteresadosForm(proy)
            
            return render_to_response('usuarios/formulario_participar.html', {"form":form},context_instance=RequestContext(request))
        
    except ObjectDoesNotExist:
        pass
    