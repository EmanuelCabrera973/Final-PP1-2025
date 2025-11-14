from django.shortcuts import render
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.urls import reverse_lazy
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin 
from django_filters.views import FilterView 


from .models import Producto
from .forms import ProductoForm
from .filters import ProductoFilter
from apps.core.mixins import StockGroupRequiredMixin

### para el jbascript ###
from django.http import JsonResponse
from .models import Producto

def productos_json(request):
    """API simple para obtener precios de productos"""
    productos = Producto.objects.filter(activo=True).values('id', 'precio')
    precios = {str(producto['id']): float(producto['precio']) for producto in productos}
    return JsonResponse(precios)

### para las vitas ###


class ProductoListView(StockGroupRequiredMixin, FilterView):
    model = Producto
    template_name = "productos/producto_list.html"
    context_object_name = "productos"
    filterset_class = ProductoFilter
    paginate_by = 10



class ProductoCreateView(StockGroupRequiredMixin, CreateView):
    model = Producto
    form_class = ProductoForm
    template_name= "productos/producto_form.html"
    success_url = reverse_lazy("productos:lista")

    def form_valid(self,form):
        messages.success(self.request, "producto creado Existosamente.")
        return super().form_valid(form)
    
class ProductoUpdateView(StockGroupRequiredMixin, UpdateView):
    model = Producto
    form_class = ProductoForm
    template_name = "productos/producto_form.html"
    success_url = reverse_lazy("productos:lista")

    def form_valid(self, form):
        messages.success(self.request, "producto Actualizado Exitosamente.")
        return super().form_valid(form)

class ProductoDeleteView(StockGroupRequiredMixin, DeleteView):
    model = Producto
    template_name = "productos/producto_confirm_delete.html"
    success_url = reverse_lazy("productos:lista")

    def delete(self, request, *args, **kwargs):
        messages.success(self.request, "Producto eliminado Exitosamente.")
        return super().delete(request, *args, **kwargs)

class ProductoDetailView(StockGroupRequiredMixin,DetailView):
    model= Producto
    template_name= "productos/producto_detail.html"
    context_objet_name = "producto"

   

# Create your views here.
