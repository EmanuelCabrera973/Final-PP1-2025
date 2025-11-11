import django_filters 
from .models import Producto

class ProductoFilter(django_filters.FilterSet):
    nombre = django_filters.CharFilter(
        lookup_expr="icontains", label= "Buscar Por Nombre"
    )
    stock_bajo = django_filters.BooleanFilter(
        method = "filter_stock_bajo", label = "Stock Bajo"
    )
    class Meta:
        model = Producto
        fields = ["nombre", "activo",]
        
    def filter_stock_bajo(self,queryset,name,value):
        if value:
            return queryset.filter(stock__lt=10)
        return quetyset
    
