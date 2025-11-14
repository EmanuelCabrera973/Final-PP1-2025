from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from .models import Cliente
from apps.core.mixins import VentasGroupRequiredMixin
from .forms import ClienteForm

class ClienteListView(VentasGroupRequiredMixin, ListView):
    model = Cliente
    template_name = "clientes/cliente_list.html"
    context_object_name = "clientes"
    paginate_by = 10

    def get_queryset(self):
        queryset = super().get_queryset()
        busqueda = self.request.GET.get("busqueda")

        if busqueda:
            queryset = queryset.filter(
                Q(nombre_icontains=busqueda) |
                Q(apellido_icontains=busqueda) |
                Q(numero_documento_icontains=busqueda) |
                Q(email_icontains=busqueda)
            )
                
        return queryset
class ClienteCreateView(VentasGroupRequiredMixin, CreateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:lista")


    def form_valid(self,form):
        messages.success(self.request,"cliente Bien Creado")
        return super().form_valid(form)
    
class ClienteUpdateView(VentasGroupRequiredMixin, UpdateView):
    model = Cliente
    form_class = ClienteForm
    template_name = "clientes/cliente_form.html"
    success_url = reverse_lazy("clientes:lista")

    def form_valid(self, form):
        messages.success(self.request, "Cliente Bien Actualizado")
        return super().form_valid(form)
    
class ClienteDeleteView(VentasGroupRequiredMixin, DeleteView ):
    models = Cliente
    template_name = "clientes/cliente_confirm_delete.html"
    success_url = reverse_lazy("clientes:lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Cliente Bien Eliminado")
        return super().delete(request, *args, **kwargs)
    
class ClienteDetailView(VentasGroupRequiredMixin, DetailView):
    model = Cliente
    template_name = "clientes/cliente_detail.html"
    context_object_name = "cliente"
    

# Create your views here.