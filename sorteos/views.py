from distutils.log import INFO
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from django.urls import reverse
from .models import Regalo, Sorteo, Participante, Exclusion
from .forms import SorteoForm, ParticipanteForm, ExclusionForm, RegisterForm
from datetime import datetime
import os,logging, hashlib
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from django.http import HttpResponse
from .random_pairs import element, random_pairs


logger = logging.getLogger(__name__)
UserModel = get_user_model()

# Create your views here.
class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'sorteos/index.html'
    context_object_name = 'user_sorteos_list'
    model = Sorteo
    #paginate_by = 10  # if pagination is desired
    ordering = ['-created']

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        

class SorteoView(LoginRequiredMixin, generic.View):

    def get(self, request):
        form = SorteoForm()
        ctx = {'form': form}
        return render(request, 'sorteos/sorteo.html', ctx)

    def post(self, request):
        form = SorteoForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, 'sorteos/sorteo.html', ctx)
        new_sorteo = form.save(commit=False)
        md5_string = str(datetime.now().timestamp()) + new_sorteo.name
        new_sorteo.md5 = hashlib.md5(md5_string.encode()).hexdigest()
        new_sorteo.owner = self.request.user
        new_sorteo.save()
        log_msg = "Nuevo evento {} creado por usuario {}".format(new_sorteo.name, self.request.user)
        logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:index'))


class DetailView(LoginRequiredMixin, generic.ListView):
    template_name = 'sorteos/detail.html'
    context_object_name = 'sorteo_participantes_list'
    model = Participante
    #paginate_by = 10  # if pagination is desired
    ordering = ['-created']

    def get_queryset(self):
        self.sorteo = get_object_or_404(Sorteo,md5=self.kwargs['md5'])
        return super().get_queryset().filter(owner=self.request.user).filter(sorteo=self.sorteo)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sorteo']=self.sorteo
        exclusiones = Exclusion.objects.filter(sorteo__md5 = self.sorteo.md5)
        context['exclusiones'] = exclusiones
        return context

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)


class ParticipanteView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        form = ParticipanteForm()
        form.sorteo = get_object_or_404(Sorteo, md5=md5)
        ctx = {'form': form, 'sorteo': form.sorteo}
        return render(request, 'sorteos/participante.html', ctx)

    def post(self, request, md5):
        form = ParticipanteForm(request.POST)
        if not form.is_valid():
            form.sorteo = get_object_or_404(Sorteo, md5=md5)
            ctx = {'form': form, 'sorteo': form.sorteo}
            return render(request, 'sorteos/participante.html', ctx)
        new_participante = form.save(commit=False)
        new_participante.owner = self.request.user
        sorteo = get_object_or_404(Sorteo, md5=md5)
        new_participante.sorteo = sorteo
        md5_string = str(datetime.now().timestamp()) + md5 + new_participante.email
        new_participante.md5 = hashlib.md5(md5_string.encode()).hexdigest()
        new_participante.save()
        sorteo.done = False
        sorteo.enviado = False
        sorteo.save()
        log_msg = "Nuevo amigo {} añadido por {} en evento {}".format(new_participante.name, self.request.user,sorteo.name)
        logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':md5} ))


class ExclusionView(LoginRequiredMixin, generic.View):

    def get(self, request, sorteo_md5, participante_md5 ):
        form = ExclusionForm(sorteo_md5, participante_md5)
        form.sorteo = get_object_or_404(Sorteo, md5=sorteo_md5)
        form.de_participante = get_object_or_404(Participante,md5=participante_md5)
        exclusiones = Exclusion.objects.filter(de_participante__md5 = participante_md5)
        ctx = {'form': form, 'sorteo': form.sorteo, 'participante': form.de_participante, 'exclusiones': exclusiones}
        return render(request, 'sorteos/exclusion.html', ctx)

    def post(self, request, sorteo_md5, participante_md5):
        for e in Exclusion.objects.filter(de_participante__md5 = participante_md5):
            e.delete()
        form = ExclusionForm(sorteo_md5, participante_md5,request.POST)
        sorteo = get_object_or_404(Sorteo, md5=sorteo_md5)
        form.sorteo = sorteo
        form.de_participante = get_object_or_404(Participante,md5=participante_md5)
        if not form.is_valid():
            ctx = {'form': form, 'sorteo': form.sorteo, 'participante':form.de_participante}
            return render(request, 'sorteos/exclusion.html', ctx)
        new_exclusion = form.save(commit=False)
        new_exclusion.owner = self.request.user
        new_exclusion.sorteo = get_object_or_404(Sorteo, md5=sorteo_md5)
        new_exclusion.de_participante = get_object_or_404(Participante, md5=participante_md5)
        md5_string = str(datetime.now().timestamp()) + sorteo_md5 + participante_md5 + new_exclusion.a_participante.md5
        new_exclusion.md5 = hashlib.md5(md5_string.encode()).hexdigest()
        new_exclusion.save()
        sorteo.done = False
        sorteo.enviado = False
        sorteo.save()
        log_msg = "Nueva exclusion creada: {}".format(new_exclusion)
        logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':sorteo_md5} ))


class BorrarParticipanteView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        participante = get_object_or_404(Participante, md5=md5)
        sorteo = get_object_or_404(Sorteo,md5=participante.sorteo.md5)
        if participante:
            participante.delete()
            sorteo.done = False
            sorteo.enviado = False
            sorteo.save()
            log_msg = "Amigo {} borrado por {} de evento {}".format(participante.name, self.request.user,sorteo.name)
            logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':sorteo.md5} ))


class BorrarExclusionView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        exclusion = get_object_or_404(Exclusion, md5=md5)
        sorteo = get_object_or_404(Sorteo,md5=exclusion.sorteo.md5)
        if exclusion:
            exclusion.delete()
            sorteo.done = False
            sorteo.enviado = False
            sorteo.save()
            log_msg = "Exclusion de {} a {} borrada por {} de evento {}".format(exclusion.de_participante, exclusion.a_participante, self.request.user,sorteo.name)
            logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':sorteo.md5} ))


class BorrarSorteoView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        sorteo = get_object_or_404(Sorteo, md5=md5)
        if sorteo:
            sorteo.delete()
            log_msg = "Evento {} eliminado por {}".format(sorteo.name, self.request.user)
            logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:index'))


class RegisterView(generic.View):

    def get(self, request):
        form = RegisterForm()
        ctx = {'form': form}
        return render(request, 'registration/register.html', ctx)

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, 'registration/register.html', ctx)
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        log_msg = "Usuario {} registrado. Cuenta no activada".format(user)
        logger.info(log_msg)
        current_site = get_current_site(request)
        mail_subject = 'Amigo Invisible - Activa tu cuenta'
        message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
        })
        to_email = form.cleaned_data.get('email')
        email = EmailMessage(
            mail_subject, message, to=[to_email]
            )
        try:
            email.send()
            log_msg = "Email de activación enviado a usuario {}".format(user)
            logger.info(log_msg)
        except Exception as e:
            logger.error(e)
        ctx = {'user': user}
        return render(request, 'registration/acc_email_confirm.html', ctx)


class ActivateView(generic.View):

    def get(self, request, uidb64, token):
        try:
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user is not None and default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            log_msg = "Usuario {} activado correctamente".format(user)
            logger.info(log_msg)
            ctx = {'user': user}
            return render(request, 'registration/acc_email_success.html', ctx)
        else:
            log_msg = "Intento de activación de usuario con uid {}".format(uid)
            logger.warn(log_msg)
            return render(request, 'registration/acc_email_fail.html')


class SortearView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        sorteo = get_object_or_404(Sorteo,md5 = md5)
        regalos = Regalo.objects.filter(sorteo = sorteo)
        if regalos:
            regalos.delete()
        participantes = Participante.objects.filter(owner=self.request.user).filter(sorteo=sorteo)
        exclusiones = Exclusion.objects.filter(owner=self.request.user).filter(sorteo=sorteo)
        elements = []
        for p in participantes:
            e = exclusiones.filter(de_participante=p)
            if e:
                elements.append(element(p.md5, e.first().a_participante.md5))
            else:
                elements.append(element(p.md5, None))
        for e in random_pairs(elements):
            md5_string = str(datetime.now().timestamp()) + sorteo.md5 + e.id + e.partner
            regalo = Regalo(
                sorteo = sorteo,
                de_participante = get_object_or_404(Participante,md5=e.id),
                a_participante = get_object_or_404(Participante,md5=e.partner),
                owner = sorteo.owner,
                md5 = hashlib.md5(md5_string.encode()).hexdigest()
            )
            regalo.save()
        sorteo.done = True
        sorteo.enviado = False
        sorteo.save()
        log_msg = "Evento {} sorteado".format(sorteo)
        logger.info(log_msg)
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':sorteo.md5} ))


class EnviarMailsView(LoginRequiredMixin, generic.View):

    def get(self, request, md5):
        sorteo = get_object_or_404(Sorteo,md5 = md5)
        if sorteo.done:
            regalos = Regalo.objects.filter(sorteo = sorteo)
            if regalos:
                for regalo in regalos:
                    mail_subject = 'Resultado Sorteo Amigo Invisible'
                    message = render_to_string('registration/acc_resultado_email.html', {
                        'user': regalo.de_participante,
                        'partner': regalo.a_participante,
                        'evento': sorteo.name,
                        'condiciones': sorteo.description,
                        })
                    to_email = regalo.de_participante.email
                    email = EmailMessage(
                        mail_subject, message, to=[to_email]
                        )
                    try:
                        email.send()
                        log_msg = "Email enviado correctamente a usuario {} para evento {}".format(regalo.de_participante, sorteo.name)
                        logger.info(log_msg)
                    except Exception as e:
                        log_msg = "Error enviando email a usuario {} para evento {}".format(regalo.de_participante, sorteo.name)
                        logger.warn(log_msg)
            sorteo.enviado = True
            sorteo.save()       
        return HttpResponseRedirect(reverse('sorteos:detail',kwargs={'md5':sorteo.md5}))