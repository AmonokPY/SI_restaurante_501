import json

from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST

from .decorators import api_login_required
from .forms import IngresoForm, RegistroAdministradorForm
from .models import Cliente, Empleado, Factura, Mesa, Orden, Plato

# =====================================
# AUTENTICACIÓN
# =====================================


def ingresar(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = IngresoForm(request, data=request.POST or None)

    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        siguiente = request.POST.get('next') or request.GET.get('next')
        if siguiente and url_has_allowed_host_and_scheme(
            siguiente,
            allowed_hosts={request.get_host()},
            require_https=request.is_secure(),
        ):
            return redirect(siguiente)
        return redirect('inicio')

    return render(request, 'gestion/ingresar.html', {'form': form})


def registro(request):
    if request.user.is_authenticated:
        return redirect('inicio')

    form = RegistroAdministradorForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(
            request,
            'Cuenta de administrador creada. Inicia sesión con tu usuario y contraseña.',
        )
        return redirect('ingresar')

    return render(request, 'gestion/registro.html', {'form': form})


@require_POST
@login_required
def salir(request):
    logout(request)
    return redirect('ingresar')

# =====================================
# INICIO
# =====================================


@login_required
def inicio(request):
    context = {
        'total_clientes': Cliente.objects.count(),
        'total_empleados': Empleado.objects.count(),
        'total_mesas': Mesa.objects.count(),
        'total_platos': Plato.objects.count(),
        'total_ordenes': Orden.objects.count(),
        'total_facturas': Factura.objects.count(),
    }

    return render(request, 'gestion/inicio.html', context)

# =====================================
# HTML
# =====================================


@login_required
def lista_clientes(request):
    return render(request, 'gestion/clientes.html')


@login_required
def lista_empleados(request):
    return render(request, 'gestion/empleados.html')


@login_required
def lista_mesas(request):
    return render(request, 'gestion/mesas.html')


@login_required
def lista_platos(request):
    return render(request, 'gestion/platos.html')


@login_required
def lista_ordenes(request):
    return render(request, 'gestion/ordenes.html')


@login_required
def lista_facturas(request):
    return render(request, 'gestion/facturas.html')

# =====================================
# CLIENTES API
# =====================================


@csrf_exempt
@api_login_required
def clientes_api(request):

    if request.method == 'GET':

        clientes = list(
            Cliente.objects.values()
        )

        return JsonResponse(clientes, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        cliente = Cliente.objects.create(
            nombre=data['nombre'],
            telefono=data['telefono'],
            correo=data['correo']
        )

        return JsonResponse({
            'mensaje': 'Cliente creado'
        })


@csrf_exempt
@api_login_required
def cliente_detalle(request, pk):

    cliente = Cliente.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        cliente.nombre = data['nombre']
        cliente.telefono = data['telefono']
        cliente.correo = data['correo']

        cliente.save()

        return JsonResponse({
            'mensaje': 'Cliente actualizado'
        })

    elif request.method == 'DELETE':

        cliente.delete()

        return JsonResponse({
            'mensaje': 'Cliente eliminado'
        })

# =====================================
# EMPLEADOS API
# =====================================


@csrf_exempt
@api_login_required
def empleados_api(request):

    if request.method == 'GET':

        empleados = list(
            Empleado.objects.values()
        )

        return JsonResponse(empleados, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        Empleado.objects.create(
            nombre=data['nombre'],
            cargo=data['cargo'],
            telefono=data['telefono'],
            correo=data['correo']
        )

        return JsonResponse({
            'mensaje': 'Empleado creado'
        })


@csrf_exempt
@api_login_required
def empleado_detalle(request, pk):

    empleado = Empleado.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        empleado.nombre = data['nombre']
        empleado.cargo = data['cargo']
        empleado.telefono = data['telefono']
        empleado.correo = data['correo']

        empleado.save()

        return JsonResponse({
            'mensaje': 'Empleado actualizado'
        })

    elif request.method == 'DELETE':

        empleado.delete()

        return JsonResponse({
            'mensaje': 'Empleado eliminado'
        })

# =====================================
# MESAS API
# =====================================


@csrf_exempt
@api_login_required
def mesas_api(request):

    if request.method == 'GET':

        mesas = list(
            Mesa.objects.values()
        )

        return JsonResponse(mesas, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        Mesa.objects.create(
            numero_mesa=data['numero_mesa'],
            capacidad=data['capacidad'],
            estado_mesa=data['estado_mesa']
        )

        return JsonResponse({
            'mensaje': 'Mesa creada'
        })


@csrf_exempt
@api_login_required
def mesa_detalle(request, pk):

    mesa = Mesa.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        mesa.numero_mesa = data['numero_mesa']
        mesa.capacidad = data['capacidad']
        mesa.estado_mesa = data['estado_mesa']

        mesa.save()

        return JsonResponse({
            'mensaje': 'Mesa actualizada'
        })

    elif request.method == 'DELETE':

        mesa.delete()

        return JsonResponse({
            'mensaje': 'Mesa eliminada'
        })

# =====================================
# PLATOS API
# =====================================


@csrf_exempt
@api_login_required
def platos_api(request):

    if request.method == 'GET':

        platos = list(
            Plato.objects.values()
        )

        return JsonResponse(platos, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        Plato.objects.create(
            nombre_plato=data['nombre_plato'],
            descripcion=data['descripcion'],
            precio=data['precio'],
            categoria=data['categoria'],
            disponible=data['disponible']
        )

        return JsonResponse({
            'mensaje': 'Plato creado'
        })


@csrf_exempt
@api_login_required
def plato_detalle(request, pk):

    plato = Plato.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        plato.nombre_plato = data['nombre_plato']
        plato.descripcion = data['descripcion']
        plato.precio = data['precio']
        plato.categoria = data['categoria']
        plato.disponible = data['disponible']

        plato.save()

        return JsonResponse({
            'mensaje': 'Plato actualizado'
        })

    elif request.method == 'DELETE':

        plato.delete()

        return JsonResponse({
            'mensaje': 'Plato eliminado'
        })

# =====================================
# ORDENES API
# =====================================


@csrf_exempt
@api_login_required
def ordenes_api(request):

    if request.method == 'GET':

        ordenes = list(
            Orden.objects.values()
        )

        return JsonResponse(ordenes, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        Orden.objects.create(
            cliente_id=data['cliente_id'],
            empleado_id=data['empleado_id'],
            mesa_id=data['mesa_id'],
            estado_orden=data['estado_orden'],
            total=data['total']
        )

        return JsonResponse({
            'mensaje': 'Orden creada'
        })


@csrf_exempt
@api_login_required
def orden_detalle(request, pk):

    orden = Orden.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        orden.cliente_id = data['cliente_id']
        orden.empleado_id = data['empleado_id']
        orden.mesa_id = data['mesa_id']
        orden.estado_orden = data['estado_orden']
        orden.total = data['total']

        orden.save()

        return JsonResponse({
            'mensaje': 'Orden actualizada'
        })

    elif request.method == 'DELETE':

        orden.delete()

        return JsonResponse({
            'mensaje': 'Orden eliminada'
        })

# =====================================
# FACTURAS API
# =====================================


@csrf_exempt
@api_login_required
def facturas_api(request):

    if request.method == 'GET':

        facturas = list(
            Factura.objects.values()
        )

        return JsonResponse(facturas, safe=False)

    elif request.method == 'POST':

        data = json.loads(request.body)

        Factura.objects.create(
            orden_id=data['orden_id'],
            subtotal=data['subtotal'],
            impuesto=data['impuesto'],
            total_factura=data['total_factura'],
            metodo_pago=data['metodo_pago']
        )

        return JsonResponse({
            'mensaje': 'Factura creada'
        })


@csrf_exempt
@api_login_required
def factura_detalle(request, pk):

    factura = Factura.objects.get(id=pk)

    if request.method == 'PUT':

        data = json.loads(request.body)

        factura.orden_id = data['orden_id']
        factura.subtotal = data['subtotal']
        factura.impuesto = data['impuesto']
        factura.total_factura = data['total_factura']
        factura.metodo_pago = data['metodo_pago']

        factura.save()

        return JsonResponse({
            'mensaje': 'Factura actualizada'
        })

    elif request.method == 'DELETE':

        factura.delete()

        return JsonResponse({
            'mensaje': 'Factura eliminada'
        })
