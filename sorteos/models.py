from django.db import models
from django.conf import settings
import datetime

# Create your models here.
class Sorteo(models.Model):
    name = models.CharField(max_length=20)
    description = models.CharField(max_length=200, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    md5 = models.SlugField(default='', max_length=32)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    done = models.BooleanField(default=False)
    enviado = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Participante(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    name = models.CharField(max_length=20)
    email = models.EmailField(blank=False)
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    md5 = models.SlugField(default='', max_length=32)
    
    def __str__(self):
        return self.name


class Exclusion(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    de_participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='de_participante')
    a_participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='a_participante')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    md5 = models.SlugField(default='', max_length=32)
    
    def __str__(self):
        return self.de_participante.name + ' no puede regalar a ' + self.a_participante.name + ' en ' + self.sorteo.name


class Regalo(models.Model):
    sorteo = models.ForeignKey(Sorteo, on_delete=models.CASCADE)
    de_participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='de_regalante')
    a_participante = models.ForeignKey(Participante, on_delete=models.CASCADE, related_name='a_regalante')
    owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    md5 = models.SlugField(default='', max_length=32)
    
    def __str__(self):
        return self.de_participante.name + ' regala a ' + self.a_participante.name + ' en ' + self.sorteo.name