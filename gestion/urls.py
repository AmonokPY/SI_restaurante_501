from django.urls import path

from . import views

urlpatterns = [

    path('cuentas/ingresar/', views.ingresar, name='ingresar'),
    path('cuentas/registro/', views.registro, name='registro'),
    path('cuentas/salir/', views.salir, name='salir'),

    path('', views.inicio, name='inicio'),

    path('clientes/', views.lista_clientes, name='clientes'),
    path('api/clientes/', views.clientes_api),
    path('api/clientes/<int:pk>/', views.cliente_detalle),

    path('empleados/', views.lista_empleados, name='lista_empleados'),
    path('api/empleados/', views.empleados_api),
    path('api/empleados/<int:pk>/', views.empleado_detalle),

    path('mesas/', views.lista_mesas, name='lista_mesas'),
    path('api/mesas/', views.mesas_api),
    path('api/mesas/<int:pk>/', views.mesa_detalle),

    path('platos/', views.lista_platos, name='lista_platos'),
    path('api/platos/', views.platos_api),
    path('api/platos/<int:pk>/', views.plato_detalle),

    path('ordenes/', views.lista_ordenes, name='lista_ordenes'),
    path('api/ordenes/', views.ordenes_api),
    path('api/ordenes/<int:pk>/', views.orden_detalle),

    path('facturas/', views.lista_facturas, name='lista_facturas'),
    path('api/facturas/', views.facturas_api),
    path('api/facturas/<int:pk>/', views.factura_detalle),
]
