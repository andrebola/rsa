# -*- encoding: utf-8 -*-
from django import forms
from proyectos.models import Empresa,Proyecto,GrupoInteres
from django.utils.translation import ugettext as _
from django.utils.html import escape
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist

class EmpresaForm(forms.Form):
        
    nombre= forms.CharField(max_length=50, min_length=1, required=False)
    email=forms.EmailField(widget = forms.TextInput(attrs = {'class':'required'}), required=True)
    password = forms.CharField(widget=forms.PasswordInput(attrs = {'class':'required'}),required=True)
        
    def __init__(self, *args, **kwargs):
        super(EmpresaForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs={'placeholder':_('Email*')}
        self.fields['password'].widget.attrs={'placeholder':_('Contrasena*')}
        self.fields['nombre'].widget.attrs={'placeholder':_('Nombre*')}
    def clean(self ):
        cleaned_data = super(EmpresaForm, self).clean()
        email = cleaned_data.get("email")
        try:
            User.objects.get(email=email)
            raise forms.ValidationError("El email ya existe")
        except ObjectDoesNotExist:
            return cleaned_data
    
        
class EmpresaModelForm(forms.ModelForm):
        
    class Meta:
        model = Empresa
    
    def __init__(self, *args, **kwargs):
        super(EmpresaModelForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs={'placeholder':_('Nombre*')}
        self.fields['descripcion'].widget.attrs={'placeholder':_('descripcion*')}
    
    def save(self):
        empresa = super(EmpresaModelForm, self).save(commit=False)
        empresa.nombre=self.cleaned_data.get('nombre')
        empresa.descripcion=self.cleaned_data.get('descripcion')
        empresa.avatar=self.cleaned_data.get('avatar')
        empresa.save()
        return empresa

class ProyectoForm(forms.ModelForm):
        
    class Meta:
        model = Proyecto
        exclude=['empresa','slug']
    def __init__(self, *args, **kwargs):
        super(ProyectoForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs={'placeholder':_('Nombre*')}
        self.fields['descripcion'].widget.attrs={'placeholder':_('descripcion*')}
        self.fields['latitud'].widget=forms.HiddenInput()
        self.fields['longitud'].widget=forms.HiddenInput()
        
        
class GrupoInteresForm(forms.ModelForm):
    class Meta:
        model = GrupoInteres
        exclude = ('proyecto',)
    
    def __init__(self, *args, **kwargs):
        super(GrupoInteresForm, self).__init__(*args, **kwargs)
        self.fields['nombre'].widget.attrs={'placeholder': 'nombre (ej: Vecinos de la zona)'}
        
        