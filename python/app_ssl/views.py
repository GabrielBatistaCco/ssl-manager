from .models import Cert
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.urls import reverse_lazy
from django.http import HttpResponseRedirect

class CertListView(ListView):
    model = Cert

class CertCreateView(CreateView):
    model = Cert
    fields = ["dominio", "url_ssls"]
    success_url = reverse_lazy("lista_ssl")

class CertUpdateView(UpdateView):
    model = Cert
    fields = ["dominio", "url_ssls"]
    success_url = reverse_lazy("lista_ssl")

class CertDeleteView(DeleteView):
    model = Cert
    success_url = reverse_lazy("lista_ssl")