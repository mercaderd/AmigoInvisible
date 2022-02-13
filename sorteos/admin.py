from django.contrib import admin
from .models import Exclusion, Sorteo,Participante, Regalo
from .forms import SorteoForm, ParticipanteForm

# Register your models here.
admin.site.register(Sorteo)
admin.site.register(Participante)
admin.site.register(Exclusion)
admin.site.register(Regalo)
