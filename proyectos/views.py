from django.shortcuts import render_to_response
from django.template import RequestContext
from proyectos.models import Proyecto
#from comunes.models import Lugar
from comunes.forms import PaisesForm
from proyectos.forms import EmpresaForm,EmpresaModelForm,ProyectoForm,GrupoInteresForm
from usuarios.models import Interesado
from proyectos.models import Empresa,GrupoInteres
from usuarios.forms import InteresadoForm,RegisterForm
from discucion.models import Grupo_Discucion
from discucion.forms import GrupoDiscucionForm
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import Q
from django.http import HttpResponseRedirect, HttpResponseForbidden, Http404, HttpResponse
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.utils.http import base36_to_int
from django.utils.translation import ugettext, ugettext_lazy as _
from django.contrib.contenttypes.models import ContentType
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator

from comunes.utils import get_default_redirect
from comunes.forms import  LoginFormulario
from django.forms.models import inlineformset_factory
from django.utils import simplejson

# Pagina principal
def landing(request):
    if request.user.is_authenticated() :
        return HttpResponseRedirect(reverse("proyectos.views.lista_proyectos"))
    
    form_int =RegisterForm()
    form_emp = EmpresaForm()
    
    if request.method == 'POST':
        form_paises = PaisesForm(request.POST)
       
        if form_paises.is_valid() :
           
            data = form_paises.cleaned_data
            proyectos= Proyecto.objects.filter(lugar=data['paises']).all()
            return render_to_response('landing.html', {'proyectos':proyectos,'form_paises':form_paises,'form_int':form_int,'form_emp':form_emp},context_instance=RequestContext(request))
        else:
            proyectos= Proyecto.objects.filter(lugar__nivel=1).filter(lugar__nombre='Chile').all()[:6]
    else:
        form_paises = PaisesForm()
        proyectos= Proyecto.objects.filter(lugar__nivel=1).filter(lugar__nombre='Chile').all()[:6]
    
    return render_to_response('landing.html', {'proyectos':proyectos,'form_paises' : form_paises, 'form_int':form_int,'form_emp':form_emp},context_instance=RequestContext(request))



# Primer paso del registo de una empresa
def registro_empresa_1(request):
    
    if request.method == 'POST':
        
        form_emp=EmpresaForm(request.POST)
        
        if form_emp.is_valid():
            data = form_emp.cleaned_data
            empresa = Empresa.create(data['nombre'])
            empresa.save() 
            user=User.objects.create(username=data['email'],email=data['email'])
            user.set_password(data['password'])
            user.save()
            user.interesado.empresa=empresa
            user.interesado.save()
            return HttpResponseRedirect("paso2/"+str(empresa.id)+"/")
        else:
            return landing(request)
    else:
        return HttpResponse('ERROR')

# Segundo paso del registo de una empresa
def paso2(request,empresa_id):
    
    empresa=Empresa.objects.get(id=empresa_id)
    
    if request.method =="POST":
        empresa_form = EmpresaModelForm(request.POST,request.FILES,instance=empresa) 
        if empresa_form.is_valid():
            empresa=empresa_form.save()
            empresa.save()
            interesado=empresa.administradores.all()[0]
            interesado.user.backend = 'django.contrib.auth.backends.ModelBackend'
            login(request,interesado.user)
            return HttpResponseRedirect(reverse("proyectos.views.crear_proyecto"))
        else:
            return HttpResponse(empresa_form.errors)
        
    else:
        empresa_form = EmpresaModelForm(instance=empresa)
        return render_to_response('proyectos/registro_paso2_emp.html', {'empresa_form':empresa_form,'empresa':empresa},context_instance=RequestContext(request))
    return HttpResponse('Error en paso 2')
  
# Perfil de un proyecto
def proyecto_perfil(request,proyecto_id):
   
    try:
        proyecto=Proyecto.objects.get(id=proyecto_id)
    except:
        return HttpResponse('proyecto no valido')
   
    if request.method == 'POST':
        
        return HttpResponse("POST")
        
    else:
        acuerdos=[]
        for grupo in proyecto.grupos.all():
            if grupo.acuerdos.all():
                acuerdos.append(grupo.acuerdos.all())
        
        return render_to_response('popup.html', {'proyecto':proyecto,'acuerdos':acuerdos},context_instance=RequestContext(request))

# Listado de proyectos
@login_required(login_url='/login_redirect/1')
def lista_proyectos(request,opcion=None):
     return render_to_response('proyectos/listado_proyectos.html', {'form_paises':PaisesForm(),'user':request.user},context_instance=RequestContext(request))
   


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')


def mylogin(request,redirect=None ,**kwargs):
    
    
    proyectos=[]
    if request.user.is_authenticated() :
        #return lista_proyectos(request,request.user.id,None)
        return HttpResponseRedirect(reverse("proyectos.views.lista_proyectos"))
    
    form_class = kwargs.pop("form_class", LoginFormulario)
    template_name = kwargs.pop("template_name", "comunes/login.html")
    success_url = kwargs.pop("success_url", 'proyectos/listado_proyectos/')
    associate_openid = kwargs.pop("associate_openid", False)
    openid_success_url = kwargs.pop("openid_success_url", None)
    url_required = kwargs.pop("url_required", False)
    extra_context = kwargs.pop("extra_context", {})
    redirect_field_name = kwargs.pop("redirect_field_name", "next")
    #return HttpResponse(redirect_field_name)
    
    if extra_context is None:
        extra_context = {}
    if success_url is None:
        success_url = get_default_redirect(request, redirect_field_name)
    
    if request.method == "POST" and not url_required:
        
        
        form = form_class(request.POST)
        if form.is_valid():
            
            form.login(request)
            #return lista_proyectos(request,request.user.id,None)
            return HttpResponseRedirect(reverse("proyectos.views.lista_proyectos"))
            #return HttpResponseRedirect(success_url)
        else:
            return render_to_response('comunes/login_redirect.html',{
            "form": form,
            "url_required": url_required,
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": request.REQUEST.get(redirect_field_name),
            },context_instance=RequestContext(request))
    else:
        
        form = LoginFormulario()
    
    if redirect :
        return render_to_response('comunes/login_redirect.html',{
        "form": form,
        "url_required": url_required,
        "redirect_field_name": redirect_field_name,
        "redirect_field_value": request.REQUEST.get(redirect_field_name),
    },context_instance=RequestContext(request))
    else:    
        return render_to_response(template_name,{
            "form": form,
            "url_required": url_required,
            "redirect_field_name": redirect_field_name,
            "redirect_field_value": request.REQUEST.get(redirect_field_name),
        },context_instance=RequestContext(request))



def json_proyectos(proyectos):
    
    response_list = []
    for p in proyectos:
        
        response = {}
        response['id']=p.id
        response['nombre']=p.nombre
        response['descripcion']=p.descripcion
        if p.avatar:
            response['avatar']=p.avatar.url
        else:
            response['avatar']="http://us.123rf.com/400wm/400/400/alexmit/alexmit1101/alexmit110100048/8781616-proyecto-de-word-con-engranajes-en-fondo-aislados-en-blanco.jpg"
        response['Empresa']=p.empresa.id
        if p.lugar:
            response['lugar']=p.lugar.id
        else:
            response['lugar']=""
        response_list.append(response)
    return HttpResponse(simplejson.dumps(response_list), mimetype='application/javascript')
    



def ajax_proyectos(request):
    
    response_list = []
    
    lastid = request.GET.get('lastid',None)
    firstid = request.GET.get('firstid',None)
    lugar = request.GET.get('pais',None)
    mis_proyectos= request.GET.get('mis_proyectos',None)
        
    if(lastid):
        proyectos=Proyecto.objects.filter(lugar__id=lugar, id__gt=lastid).order_by('id')[:6]
        if proyectos.count() > 0:
            return json_proyectos(proyectos)
        else:  
            return HttpResponse('')
    elif(firstid):
        proyectos=Proyecto.objects.filter(lugar__id=lugar, id__lt=firstid).order_by('id')[:6]
        if proyectos.count() > 0:
            return json_proyectos(proyectos)
        else:
            return HttpResponse('')
    else:
        return HttpResponse('ERROR')

def ajax_mis_proyectos(request):

    lastid = request.GET.get('lastid',None)
    firstid = request.GET.get('firstid',None)
    
    if(lastid):
        
        if(request.user.interesado.empresa):
        
            proyectos=request.user.interesado.empresa.proyectos.filter(id__gt=lastid).order_by('id')[:6]
            if proyectos.count() > 0:
                return json_proyectos(proyectos)
            else:  
                return HttpResponse('')
        else:   
            proyectos=request.user.interesado.proyectos_interes.filter(id__gt=lastid).order_by('id')[:6]
            if proyectos.count() > 0:
                return json_proyectos(proyectos)
            else:  
                return HttpResponse('')
       
        return json_proyectos(proyectos)
        
    elif(firstid):
        
        if(request.user.interesado.empresa):
            
            proyectos=request.user.interesado.empresa.proyectos.filter(id__lt=firstid).order_by('id')[:6]
            if proyectos.count() > 0:
                return json_proyectos(proyectos)
            else:
                return HttpResponse('')
        
        else:
            proyectos=request.user.interesado.proyectos_interes.filter(id__lt=firstid).order_by('id')[:6]
            if proyectos.count() > 0:
                return json_proyectos(proyectos)
            else:
                return HttpResponse('')
        
        
        return json_proyectos(proyectos)
    else:
        return HttpResponse('ERROR')


# Crear proyecto
def crear_proyecto(request):
    
    if request.user.interesado.empresa :
        GrupoDiscucionFormSet = inlineformset_factory(Proyecto, Grupo_Discucion,form=GrupoDiscucionForm,extra=2,can_delete=False)
        
        GrupoInteresFormSet = inlineformset_factory(Proyecto, GrupoInteres,form=GrupoInteresForm,extra=2,can_delete=False)
        if request.method == 'POST':
            g_interes_formSet = GrupoInteresFormSet(request.POST)
            g_discucion_formSet = GrupoDiscucionFormSet(request.POST)
            
            form=ProyectoForm(request.POST,request.FILES)
            if form.is_valid() and  g_interes_formSet.is_valid() and g_discucion_formSet.is_valid():
                
                proy=form.save(commit=False)
                proy.empresa=request.user.interesado.empresa
                proy.save()
                instances = g_interes_formSet.save(commit=False)    
                for g_interes in instances:
                    g_interes.proyecto = proy
                    g_interes.save()
                instances = g_discucion_formSet.save(commit=False)    
                for g_discucion in instances:
                    g_discucion.proyecto = proy
                    g_discucion.save()
                return HttpResponseRedirect(reverse("proyectos.views.lista_proyectos"))
        else:
            form=ProyectoForm()
            g_interes_formSet = GrupoInteresFormSet()
            g_discucion_formSet = GrupoDiscucionFormSet()
        return render_to_response("proyectos/crear.html",{
            "form": form,
            "g_interes_formSet": g_interes_formSet,
            "g_discucion_formSet":g_discucion_formSet,
        },context_instance=RequestContext(request))
    else :
        return HttpResponse('No puede crear proyectos')


