from hashlib import md5
from django.forms import ModelForm, EmailField
from .models import Sorteo, Participante, Exclusion
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegisterForm(UserCreationForm):
    email = EmailField()
    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]


class SorteoForm(ModelForm):
    class Meta:
        model = Sorteo
        fields = ['name', 'description']

    def __init__(self, *args, **kwargs):
        super(SorteoForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'name', 'placeholder': 'Name'})
        self.fields['description'].widget.attrs.update({'id': 'description', 'placeholder': 'Description'})


class ParticipanteForm(ModelForm):
    class Meta:
        model = Participante
        fields = ['name', 'email']

    def __init__(self, *args, **kwargs):
        super(ParticipanteForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs.update({'id': 'name', 'placeholder': 'Name'})
        self.fields['email'].widget.attrs.update({'id': 'email', 'placeholder': 'Email'})


class ExclusionForm(ModelForm):
    
    class Meta:
        model = Exclusion
        fields = ['a_participante']

    def __init__(self, sorteo_md5, participante_md5, *args, **kwargs):
        super(ExclusionForm, self).__init__(*args, **kwargs)
        self.fields['a_participante'].queryset = Participante.objects.filter(sorteo__md5=sorteo_md5).exclude(md5=participante_md5)
        self.fields['a_participante'].widget.attrs.update({'class': 'form-control'})
        
