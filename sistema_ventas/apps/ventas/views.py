from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import get_object_or_404
from django.db import transaction

from .models import Venta, ItemVenta
from .forms import VentaForm, ItemVentaFormSet
from apps.productos.models import Producto
from apps.core.mixins import VentasGroupRequiredMixin


class VentaListView(VentasGroupRequiredMixin, ListView):
    model = Venta
    form_class = VentaForm
    template_name = "ventas/venta_list.html"
    context_object_name = "ventas"
    paginate_by = 10

class VentaCreateView(VentasGroupRequiredMixin, CreateView):
    model = Venta
    form_class = VentaForm
    template_name = 'ventas/venta_form.html'
    success_url = reverse_lazy('ventas:lista')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if self.request.POST:
            context['formset'] = ItemVentaFormSet(self.request.POST)
        else:
            context['formset'] = ItemVentaFormSet()
        return context
    
    def form_valid(self, form):
        context = self.get_context_data()
        formset = context['formset']
        
        with transaction.atomic():
            # Generar código de venta automáticamente
            form.instance.codigo_venta = f"V-{Venta.objects.count() + 1:04d}"
            
            if formset.is_valid():
                self.object = form.save()
                
                # Filtrar forms vacíos antes de guardar
                form_validos = []
                for form_item in formset:
                    #solo los forms con productos
                    if (form_item.cleaned_data and not form_item.cleaned_data.get("DELETE", False)):
                        producto = form_item.cleaned_data.get("producto")
                        cantidad = form_item.cleaned_data.get("cantidad")
                        #solo agregar si tiene los 2 valores
                        if producto and cantidad:
                            form_validos.append(form_item)
                    
                if not form_validos:
                    form.add_error(None, "Debe agregar al menos un item de venta válido.")
                    return self.form_invalid(form)
                

                # Guardar solo los forms válidos
                
                for form_item in form_validos:
                    item = form_item.save(commit=False)
                    item.venta = self.object
                    # Establecer precio unitario desde el producto
                    item.precio_unitario = item.producto.precio
                    item.save()
                    
                    # Descontar stock
                    producto = item.producto
                    producto.stock -= item.cantidad
                    producto.save()
                
                messages.success(self.request, 'Venta registrada exitosamente.')
                return super().form_valid(form)
            else:
                return self.form_invalid(form)


class VentaDetailView(VentasGroupRequiredMixin, DetailView):
    model = Venta
    template_name = 'ventas/venta_detail.html'
    context_object_name = 'venta'
    
    def get_queryset(self):
        return Venta.objects.prefetch_related('items__producto')
    
    
# Create your views here.
