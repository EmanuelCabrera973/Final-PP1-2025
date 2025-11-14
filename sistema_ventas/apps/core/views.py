from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect

class HomeView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'
    
    def get(self, request, *args, **kwargs):
        # Redirigir según los permisos del usuario
        if request.user.is_superuser or request.user.groups.filter(name='administradores').exists():
            # Administradores van a producto
            return redirect('productos:lista')
        elif request.user.groups.filter(name='stock').exists():
            # Usuarios stock van a productos
            return redirect('productos:lista')
        elif request.user.groups.filter(name='ventas').exists():
            # Usuarios ventas van a ventas
            return redirect('ventas:lista')
        else:
            # Usuarios sin grupo van a productos
            return redirect('productos:lista')