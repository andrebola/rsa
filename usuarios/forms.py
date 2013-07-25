# -*- coding: utf-8 -*-
from django import forms
from models import Interesado,RelacionInteresados
from django.utils.translation import ugettext as _
from django.utils.html import escape
from django.contrib.auth.models import User
from django.http import HttpResponse
#from registration.forms import RegistrationForm


class RelacionInteresadosForm(forms.ModelForm):
    class Meta:
        model =RelacionInteresados
        exclude = ('interesado','proyecto',)
    def __init__(self,proyecto, *args, **kwargs):

        super(RelacionInteresadosForm, self).__init__(*args, **kwargs)
        
        self.fields['grupo_interes'].queryset=proyecto.grupo_interes


class InteresadoForm(forms.ModelForm):
        
    class Meta:
        model = Interesado
        exclude = ('user','empresa','proyectos_interes')
        
    def __init__(self, *args, **kwargs):
        super(InteresadoForm, self).__init__(*args, **kwargs)
        self.fields['lugar'].widget.attrs={'placeholder':_('Lugar de residencia')}
        self.fields['avatar'].widget.attrs={'placeholder':_('Foto de perfil')}
        self.fields['genero'].widget.attrs={'placeholder':_('Genero')}
        self.fields['ocupacion'].widget.attrs={'placeholder':_('Ocupacion')}
        self.fields['direccion'].widget.attrs={'placeholder':_('Direccion')}
        
    def save(self):
        interesado = super(InteresadoForm, self).save(commit=False)
        interesado.genero=self.cleaned_data.get('genero')
        interesado.avatar=self.cleaned_data.get('avatar')
        interesado.lugar=self.cleaned_data.get('lugar')
        interesado.edad=self.cleaned_data.get('edad')
        interesado.save()
        return interesado
    
class RegisterForm(forms.ModelForm):
  
    class Meta:
        model = User
        fields = ('email','first_name','last_name','password')
        widgets = {
            'password': forms.PasswordInput(),
        }
        
    def __init__(self, *args, **kwargs):
        super(RegisterForm, self).__init__(*args, **kwargs)
        self.fields['email'].widget.attrs={'placeholder':_('Email*')}
        self.fields['password'].widget.attrs={'placeholder':_('Contrasena*')}
        self.fields['first_name'].widget.attrs={'placeholder':_('Nombre*')}
        self.fields['last_name'].widget.attrs={'placeholder':_('Apellido*')}
        
        
        
    def clean_email(self):
        email = self.cleaned_data["email"]
        users_found = User.objects.filter(email__iexact=email)
        if len(users_found) >= 1:
            raise forms.ValidationError(_("A user with that email already exists."))
        return email


    def save(self):
        user = super(RegisterForm, self).save(commit=False)
        user.set_password(self.cleaned_data["password"])
        user.email = self.cleaned_data["email"]
        user.is_active = False
        user.username=user.email
        user.save()
        return user