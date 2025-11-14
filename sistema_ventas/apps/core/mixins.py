from django.contrib.auth.mixins import UserPassesTestMixin
from django.shortcuts import redirect
from django.urls import reverse

class GroupRequiredMixin(UserPassesTestMixin):
    """Mixin para requerir que el usuario pertenezca a un grupo específico"""
    group_required = None
    permission_denied_message = 'No tienes permisos para acceder a esta página.'
    
    def test_func(self):
        if self.group_required is None:
            return True
        
        if not self.request.user.is_authenticated:
            return False
            
         # SUPERUSERS y administradores tienen acceso a todo
        if self.request.user.is_superuser or self.request.user.groups.filter(name='administradores').exists():
            return True
            
        return self.request.user.groups.filter(name=self.group_required).exists()
    
    def handle_no_permission(self):
        from django.contrib import messages
        
        if not self.request.user.is_authenticated:
            # Usuario no autenticado - redirigir a login
            return redirect('account_login')
        else:
            # Usuario autenticado pero sin permisos - mostrar mensaje y redirigir a home
            messages.error(self.request, self.permission_denied_message)
            return redirect('home')

class StockGroupRequiredMixin(GroupRequiredMixin):
    group_required = 'stock'

class VentasGroupRequiredMixin(GroupRequiredMixin):
    group_required = 'ventas'