# -*- encoding: utf-8 -*-
from django import forms
from models import Lugar
from django.utils.translation import ugettext_lazy as _, ugettext
#from django.contrib.auth import authenticate
from django.contrib.auth import authenticate, login 

class PaisesForm(forms.Form):
    
    pais_choices=[]
    
    var = Lugar.objects.filter(nivel = 1)
    if var:
        for i in range(var.count()):
            pais_choices.extend([(str(var[i].id),var[i].nombre)])
    
    paises = forms.ChoiceField(choices=pais_choices, widget=forms.Select(attrs={'class':'selector'}))
    
    def __init__(self,*args,**kwargs):
        super(PaisesForm,self). __init__(*args,**kwargs)
   



class LoginFormulario(forms.Form):
    
    email = forms.EmailField()
    
    password = forms.CharField(
        label = _("Contrasena"),
        widget = forms.PasswordInput()
    )
    
    remember = forms.BooleanField(
        label = "Recordarme en esta máquina.",
        help_text = "Si seleccionás esta opción tu sesión quedará abierta durante 3 semanas.",
        required = False
    )
    
    user = None
    
    def __init__(self, *args, **kwargs):
        super(LoginFormulario, self).__init__(*args, **kwargs)
       
        self.fields['email'].widget.attrs={'class':'text-user','placeholder': 'email'}
        self.fields['password'].widget.attrs={'class':'text-password','placeholder': 'password'}
       
    def clean(self):
        if self._errors:
            return
        user = authenticate(username=self.cleaned_data["email"],password=self.cleaned_data["password"])
        if user:
            if user.is_active:
                self.user = user
            else:
                raise forms.ValidationError(_("This account is currently inactive."))
        else:
            error = _("The username and/or password you specified are not correct.")
            raise forms.ValidationError(error)
        return self.cleaned_data
    
    def login(self, request):
        
        login(request, self.user)
        if self.cleaned_data["remember"]:
            request.session.set_expiry(60 * 60 * 24 * 7 * 3)
        else:
            request.session.set_expiry(0)