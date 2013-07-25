from django.shortcuts import render_to_response
from django.template import RequestContext
from proyectos.models import Proyecto
from models import Grupo_Discucion, Publicacion, Comentario
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.core.urlresolvers import reverse
from forms import AcuerdoForm

# Mostrar una discucion
@login_required
def discucion(request,slug,slug_grupo):

    try:
        
        grupo = Grupo_Discucion.objects.get(proyecto__slug=slug,slug=slug_grupo)
        proyecto=grupo.proyecto
        
        orgs = proyecto.interesados.filter(id=request.user.interesado.id)
        if orgs or request.user.interesado.empresa == grupo.proyecto.empresa:
            if request.method == 'POST':
                contenido=request.POST.get('content')
                if contenido:
                    lado=False
                    if request.user.interesado.empresa == grupo.proyecto.empresa:
                        lado=True
                    pub=Publicacion.objects.create(contenido=contenido,publisher=request.user,grupo_discucion=grupo,es_empresa=lado)
                    return HttpResponseRedirect(reverse("discucion.views.discucion",args=(slug,slug_grupo)))
            
            return render_to_response('discucion/intercambio.html', {'proyecto':proyecto,"grupo":grupo},context_instance=RequestContext(request))
        else:
            pass
    except ObjectDoesNotExist:
        pass
        
        
# Ayax para comentar en una publicacion
@login_required
def comentar(request,p_id):
    try:
        pub = Publicacion.objects.get(id=p_id)
        orgs = pub.grupo_discucion.proyecto.interesados.filter(id=request.user.interesado.id)
        if orgs or request.user.interesado.empresa == pub.grupo_discucion.proyecto.empresa:
        
            if request.method == 'POST':
                contenido=request.POST.get('comm')
                if contenido:
                    lado=False
                    if request.user.interesado.empresa == pub.grupo_discucion.proyecto.empresa:
                        lado=True
                    commentario=Comentario.objects.create(contenido=contenido,autor=request.user,publicacion=pub,es_empresa=lado)
                    return render_to_response('discucion/comment.html', {'comm':commentario,"proyecto":pub.grupo_discucion.proyecto},context_instance=RequestContext(request))
        else:
            pass
    except ObjectDoesNotExist:
        pass
    
# Ver listado de acuerdos de un grupo
@login_required
def acuerdos(request,slug,slug_grupo):
    
    try:
        
        grupo = Grupo_Discucion.objects.get(proyecto__slug=slug,slug=slug_grupo)
        proyecto=grupo.proyecto
        orgs = proyecto.interesados.filter(id=request.user.interesado.id)
        if orgs or request.user.interesado.empresa == grupo.proyecto.empresa:
            if request.method == 'POST':
                form=AcuerdoForm(request.POST)
                if form.is_valid():
                    if request.user.interesado.empresa == grupo.proyecto.empresa:
                        acuerdo=form.save(commit=False)
                        acuerdo.grupo_discucion=grupo
                        acuerdo.save()
                    return HttpResponseRedirect(reverse("discucion.views.acuerdos",args=(slug,slug_grupo)))
            else:
                form=AcuerdoForm()
            return render_to_response('discucion/acuerdos.html', {'proyecto':proyecto,"grupo":grupo,"form":form,"pagina_acuerdos":True},context_instance=RequestContext(request))
        else:
            pass
    except ObjectDoesNotExist:
        pass
@login_required
def discucion_gral(request,slug):
    proy = Proyecto.objects.get(slug=slug)
    if proy.grupos:
        return discucion(request,slug,proy.grupos.all()[:1].get().slug)
