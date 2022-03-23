from django.urls import path

from . import views

app_name = 'sorteos'
urlpatterns = [
    path('', views.LandingView.as_view(), name='landing'),
    path('amin', views.IndexView.as_view(), name='index'),
    path('sorteo/', views.SorteoView.as_view(), name='sorteo'),
    path('sorteo/<slug:md5>/', views.DetailView.as_view(), name='detail'),
    path('sortear/<slug:md5>/', views.SortearView.as_view(), name='sortear'),
    path('mails/<slug:md5>/', views.EnviarMailsView.as_view(), name='mails'),
    path('participante/<slug:md5>/', views.ParticipanteView.as_view(), name='participante'),
    path('participanteborrar/<slug:md5>/', views.BorrarParticipanteView.as_view(), name='participanteborrar'),
    path('sorteoborrar/<slug:md5>/', views.BorrarSorteoView.as_view(), name='sorteoborrar'),
    path('exclusion/<slug:sorteo_md5>/<slug:participante_md5>/', views.ExclusionView.as_view(), name='exclusion'),
    path('exclusionborrar/<slug:md5>/', views.BorrarExclusionView.as_view(), name='exclusionborrar'),
    path('register/',views.RegisterView.as_view(), name = 'register'),
    path('activate/<uidb64>/<token>/',views.ActivateView.as_view(), name='activate'),
    path('about/', views.AboutView.as_view(), name='about'),
]