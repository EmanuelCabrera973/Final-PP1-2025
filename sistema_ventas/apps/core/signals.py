from django.db.models.signals import post_migrate
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.dispatch import receiver
from apps.productos.models import Producto
from apps.clientes.models import Cliente
from apps.ventas.models import Venta, ItemVenta

@receiver(post_migrate)
def create_user_groups(sender, **kwargs):
    """Crear grupos automáticamente después de las migraciones"""
    
    # Grupo Administradores - Todos los permisos
    admin_group, created = Group.objects.get_or_create(name='administradores')
    if created:
        print("Grupo 'administradores' creado")
    
    # Grupo Stock - Permisos de productos
    stock_group, created = Group.objects.get_or_create(name='stock')
    if created:
        # Permisos para Producto
        producto_permissions = Permission.objects.filter(
            content_type__model='producto',
            codename__in=['add_producto', 'change_producto', 'delete_producto', 'view_producto']
        )
        stock_group.permissions.set(producto_permissions)
        print("Grupo 'stock' creado con permisos de productos")
    
    # Grupo Ventas - Permisos de clientes y ventas
    ventas_group, created = Group.objects.get_or_create(name='ventas')
    if created:
        # Permisos para Cliente
        cliente_permissions = Permission.objects.filter(
            content_type__model='cliente',
            codename__in=['add_cliente', 'change_cliente', 'delete_cliente', 'view_cliente']
        )
        # Permisos para Venta
        venta_permissions = Permission.objects.filter(
            content_type__model='venta',
            codename__in=['add_venta', 'change_venta', 'delete_venta', 'view_venta']
        )
        # Permisos para ItemVenta
        item_venta_permissions = Permission.objects.filter(
            content_type__model='itemventa',
            codename__in=['add_itemventa', 'change_itemventa', 'delete_itemventa', 'view_itemventa']
        )
        
        # Combinar todos los permisos
        all_permissions = list(cliente_permissions) + list(venta_permissions) + list(item_venta_permissions)
        ventas_group.permissions.set(all_permissions)
        print("Grupo 'ventas' creado con permisos de clientes y ventas")