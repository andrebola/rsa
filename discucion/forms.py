from django import forms
from discucion.models import Acuerdo, Grupo_Discucion
        
        
    
class AcuerdoForm(forms.ModelForm):
    class Meta:
        model = Acuerdo
        fields = ['titulo', 'descripcion','fecha','estado_problema','nivel_criticidad',]

    def __init__(self, *args, **kwargs):
        
        super(AcuerdoForm, self).__init__(*args, **kwargs)
        
        self.fields['descripcion'].widget.attrs={'class': "wysihtml5 span12"}
        self.fields['descripcion'].widget.attrs={'placeholder': "Descripcion"}
        self.fields['titulo'].widget.attrs={'class': "span10"}
        self.fields['titulo'].widget.attrs={'placeholder': "Titulo"}
        
        

class GrupoDiscucionForm(forms.ModelForm):
    class Meta:
        model = Grupo_Discucion
        fields = ['nombre', ]
    def __init__(self, *args, **kwargs):
        
        super(GrupoDiscucionForm, self).__init__(*args, **kwargs)
        
        self.fields['nombre'].widget.attrs={'placeholder': "nombre (ej: Medio ambiente)"}
