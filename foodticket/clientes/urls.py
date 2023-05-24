from django.urls import path
from . import views

app_name = "clientes"
urlpatterns = [
    path('', views.index, name="index"),
    path('compra/', views.compra, name="compra"),
    path('compra/<int:cliente_id>/tiqueteras/', views.seleccionar_tiquetera, name='seleccionar_tiquetera'),
    path('compra/<int:cliente_id>/menus/', views.seleccionar_menu, name='seleccionar_menu'),
    path('venta/', views.venta, name="venta"),
    path('compra/informacion_cliente/', views.informacion_cliente, name='informacion_cliente'),

]