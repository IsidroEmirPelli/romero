from django.shortcuts import render, redirect
from .forms import PacienteForm, VisitaForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paciente, Visita
from .serializer import PacienteSerializer
from datetime import datetime
from .scripts.data_visualization import *
from rest_framework import status
import pandas as pd
from sqlite3 import connect


def inicio(request):
    """ Muestra la ventana de inicio """
    return render(request, 'crudromero/index.html')


def registro(request):
    """ Registra a los usuarios a través de una petición POST.
    Si los datos del formulario son correctos estos se guardan en la base de datos.
    El 'context' de la template contiene el valor del texto del botón.
    """
    if request.method == 'POST':
        # Obtengo los datos del formulario y realizo la verificación.
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()  # Guardo en la base de datos.
            return redirect('inicio')
        else:
            print(form.errors)

    # 'Registro' y 'Modificar' utilizan la misma plantilla.
    # Ya que me encuentro en 'Registro', el texto del botón será 'Agregar'.
    context = {'button': 'Agregar', 'rango': [
        "F-%.2d" % i for i in range(100)]}

    return render(request, 'crudromero/registro.html', context)


def vista(request, id):
    """ Recibe la id del paciente a mostrar, realiza la búsqueda en la base de datos,
    y si el paciente realizó más de una visita, también se buscan las fechas de estas.
    """
    paciente = Paciente.objects.get(id=id)
    print(paciente.visitas)
    visitas = Visita.objects.filter(
        paciente_id=paciente) if paciente.visitas else None  # Si realizó más de una visita, accedo a la tabla 'Visita'.
    context = {
        # Datos del paciente (contiene la primer visita).s
        'paciente': paciente,
        # Todas sus visitas (menos la primera) con fecha y hora.
        'visitas': visitas,
    }

    return render(request, 'crudromero/ver.html', context)


def get_query_result(text, all=False, fin=0, anchor=None, grow_value=100):
    """ Devuelve una consulta con la cantidad de pacientes deseados.
        Parámetros:
            text: Lista con el DNI y Nombre del paciente.
            all: Booleano que indica si se debe devolver una query con la cantidad definida por 'grow_value'.    
            fin:  Indica el último valor del valor inicial del rango de búsqueda.
            anchor: Controla el `volver a página anterior` o `página siguiente` según su valor ('next' o 'back').
            grow_value: Es la cantidad de elementos que se consultarán.
    """

    # Obtiene el límite de la consulta.
    # Si no se desea obtener 'todo', sólamente se consultan 5 elementos.
    start_value, limit = (0, 5) if not all else (
        fin, fin + grow_value) if anchor == 'next' else (fin - (grow_value*2), fin - grow_value)

    # Si se realizó la búsqueda con un solo dato, verifico si es el `DNI` o el `Nombre`.
    if text[1] == 'undefined':
        if text[0].isdigit():
            pacientes = Paciente.objects.filter(dni__startswith=text[0])[
                start_value:limit+1]
        else:
            pacientes = Paciente.objects.filter(apellido__startswith=text[0])[
                start_value:limit+1]
    else:
        # Si se realizó la búsqueda con 2 datos, verifico cuál es el `DNI` y cuál el `Nombre`.
        if text[0].isdigit():
            # Obtengo 1 dato más que el límite para saber si quedaron más pacientes.
            pacientes = Paciente.objects.filter(
                dni__startswith=text[0], apellido__startswith=text[1])[start_value:limit+1]
        else:
            pacientes = Paciente.objects.filter(
                dni__startswith=text[1], apellido__startswith=text[0])[start_value:limit+1]

    # Verficio si quedaron más pacientes.
    # Esto es para saber cuándo dejar de mostrar el botón "Página siguiente".
    more = len(pacientes) == (limit-start_value)+1 and len(pacientes) != 0

    # Devuelvo los pacientes sin el último dato, el nuevo valor inicial del rango, y la variable
    # para saber si quedaron más pacientes para consultar.
    return pacientes[:limit-start_value], limit, more


def ver_todo(request, text, fin, anchor):
    """ Devuelve la cantidad de pacientes disponibles dentro del rango definido por
    'grow_values'. En caso de haber más, se habilitará un botón para realizar otra consulta con los 
    mismos datos ya consultados (DNI/Nombre).
    """

    grow_value = 100  # Cantidad de elementos que devolverá la vista.

    # Obtengo los datos de la consulta.
    pacientes, fin, more = get_query_result(
        text.split('-'), True, fin, anchor, grow_value)

    context = {
        'text': text,
        'fin': fin,
        'pacientes': pacientes,
        # Valores para ocultar/mostrar los botones de `página anterior` o `página siguiente`.
        'd_none_back': ('d-none' if fin == grow_value else ''),
        'd_none_next': ('d-none' if not more else ''),
    }

    return render(request, 'crudromero/ver_todo.html', context)


def modificar(request, id):
    """ Actualiza los datos del paciente guardado en la base de datos
    con la nueva información modificada.
    """
    paciente = Paciente.objects.get(id=id)
    data = request.POST.dict()
    data.update({'visitas': paciente.visitas})
    if request.method == 'POST':
        form = PacienteForm(data, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('inicio')

    # El valor del botón de la ventana tendrá el texto 'Modificar' (ya que se comparte
    # el template con la función de 'Registro').
    context = {'paciente': paciente, 'button': 'Guardar cambios', 'rango': [
        "F-%.2d" % i for i in range(100)]}

    return render(request, 'crudromero/registro.html', context)


def estadisticas(request):
    """ Creación y vista de las estadísticas de datos. Si la base de datos
    está vacía, muestra una ventana indicándolo. 
    """

    conn = connect('db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM crudromero_paciente", conn)
    df_visitas = pd.read_sql_query('SELECT * FROM crudromero_visita', conn)
    conn.close()

    # Si la base de datos se encontraba vacía, muestro una página que indique esto.
    if df.empty:
        return render(request, 'crudromero/no_data.html')
    else:
        import json
        involuntario, voluntario, no = get_all_internaciones(df)
        context = {'total': voluntario + involuntario + no}
        if involuntario + voluntario > 0:
            context['torta_internados'] = json.dumps(torta_internados(
                involuntario, voluntario))
        else:
            context['torta_internados'] = None
        context['torta_pacientes_total_internados'] = json.dumps(torta_pacientes_total_internados(
            context['total'], involuntario + voluntario))
        context['torta_pacientes_por_derivacion'] = json.dumps(get_data_torta(
            df, 'derivacion'))
        context['torta_por_region_sanitaria'] = json.dumps(get_data_torta(
            df, 'region_sanitaria'))
        context['torta_por_barrio'] = json.dumps(get_data_torta(df, 'barrio'))
        context['get_days_data'] = json.dumps(get_days_data(df, df_visitas))

        return render(request, 'crudromero/estadisticas.html', context)


def nueva_visita(request, id):
    """ Añado una nueva visita a la tabla 'Visita', con la fecha y hora actual. Relaciono
    la nueva fila de la tabla con el paciente al que pertenecen estos datos.
    """
    if request.method == 'POST':
        paciente = Paciente.objects.get(id=id)
        # Si el paciente no realizó más de 1 visita, cambio el valor de la variable que
        # me indica esto.
        if not paciente.visitas:
            paciente.visitas = True
            paciente.save()

        data = request.POST.dict()
        now = datetime.now()  # Obtengo la fecha y hora actual.
        data.update({'paciente_id': paciente})
        data.update({'fecha': now.date()})
        data.update({'hora': now.strftime("%H:%M")})
        form = VisitaForm(data)

        if form.is_valid():
            form.save()
    return redirect('inicio')


@api_view(['GET'])
def get_data(request):
    """ Retorna 5 pacientes según un conjunto 'DNI-NOMBRE' ó 'NOMBRE-DNI' recibido a través
    de la petición.
    """
    # Retorna toda la información de los pacientes. que coincidan con el DNI o el Nombre.
    text = request.GET['text'].split('-')
    pacientes, _, _ = get_query_result(text, False)
    serializer = PacienteSerializer(pacientes, many=True)

    # Retorna los datos en un diccionario.
    return Response(serializer.data)


@api_view(['DELETE'])
def eliminar(request, id):
    """ Elimina al paciente de la `id` proporcionada. """
    if request.method == 'DELETE':
        paciente = Paciente.objects.get(id=id)
        paciente.delete()

        return Response(status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
