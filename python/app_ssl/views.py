from .models import Cert
from .get_ssl import GetSSLCert
# from django.views.generic import ListView, CreateView, UpdateView, DeleteView, View
from django.shortcuts import render
# , get_object_or_404, redirect
# from django.urls import reverse, reverse_lazy
# from django.http import HttpResponseRedirect
from rest_framework import viewsets
from .serializers import CertSerializer

class CertViewSet(viewsets.ModelViewSet):
    queryset = Cert.objects.all()
    serializer_class = CertSerializer

    def perform_create(self, serializer):
        dominio = serializer.validated_data.get('dominio')

        get_ssl = GetSSLCert(dominio)
        resultado_ssl = get_ssl.get_certificado()

        serializer.validated_data.update(resultado_ssl)

        super().perform_create(serializer)

    def perform_update(self, serializer):
        dominio = serializer.validated_data.get('dominio')

        get_ssl = GetSSLCert(dominio)
        resultado_ssl = get_ssl.get_certificado()

        serializer.validated_data.update(resultado_ssl)

        super().perform_update(serializer)

# class CertListView(ListView):
#     model = Cert
#     fields = ["dominio", "url_ssls"]
#     success_url = reverse_lazy("lista_ssl")
#     # context_object_name = 'cert_list'
#     # paginate_by = 15

#     # def get_queryset(self):
#     #     query = self.request.GET.get('pesquisa')
#     #     if query and len(query) >= 4:
#     #         return Cert.objects.filter(dominio__icontains=query)
#     #     return Cert.objects.all()

# class CertCreateView(CreateView):
#     model = Cert
#     fields = ['dominio', 'url_ssls']
#     success_url = reverse_lazy("lista_ssl")

#     def form_valid(self, form):
#         dominio = form.cleaned_data['dominio']

#         cert_exists = Cert.objects.filter(dominio=dominio).exists()

#         if cert_exists:
#             cert_obj = get_object_or_404(Cert, dominio=dominio)
#             edit_url = reverse('editar_ssl', kwargs={'pk': cert_obj.pk})
            
#             return redirect(edit_url)
#         else:
#             get_ssl = GetSSLCert(dominio)
#             resultado_ssl = get_ssl.get_certificado()

#             form.instance.__dict__.update(**resultado_ssl)

#             return super().form_valid(form)

# class CertUpdateView(UpdateView):
#     model = Cert
#     fields = ['dominio', 'url_ssls']
#     success_url = reverse_lazy("lista_ssl")

#     def form_valid(self, form):
#         dominio = form.cleaned_data['dominio']
#         get_ssl = GetSSLCert(dominio)

#         resultado_ssl = get_ssl.get_certificado()
#         form.instance.__dict__.update(**resultado_ssl)

#         return super().form_valid(form)

# class CertDeleteView(DeleteView):
#     model = Cert
#     success_url = reverse_lazy("lista_ssl")