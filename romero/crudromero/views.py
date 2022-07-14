from django.shortcuts import render, redirect
from .forms import PacienteForm
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Paciente
from .serializer import PacienteSerializer

def inicio(request):
    return render(request, 'crudromero/index.html')


def registro(request):
    if request.method == 'POST':
        print(request.POST.get)
        form = PacienteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('inicio')
        else:
            print(form.errors)

    context = {'button': 'Agregar'}
    return render(request, 'crudromero/registro.html', context)

def vista(request, id):
    context = {'paciente': Paciente.objects.get(id=id)}
    return render(request, 'crudromero/ver.html', context)

def get_query_result(text, all=False, fin=0, anchor=None, grow_value=100):

    start_value, limit = (0, 5) if not all else (fin, fin + grow_value) if anchor == 'next' else (fin - (grow_value*2), fin - grow_value)

    if text[1] == 'undefined':
        if text[0].isdigit():
            pacientes = Paciente.objects.filter(dni__startswith=text[0])[start_value:limit+1]
        else:
            pacientes = Paciente.objects.filter(nombre__startswith=text[0])[start_value:limit+1]
    else:
        if text[0].isdigit():
            pacientes = Paciente.objects.filter(dni__startswith=text[0], nombre__startswith=text[1])[start_value:limit+1]
        else:
            pacientes = Paciente.objects.filter(dni__startswith=text[1], nombre__startswith=text[0])[start_value:limit+1]
    
    
    more = len(pacientes) == (limit-start_value)+1 and len(pacientes) != 0

    return pacientes[:limit-start_value], limit, more

def ver_todo(request, text, fin, anchor):

    grow_value = 100

    pacientes, fin, more = get_query_result(text.split('-'), True, fin, anchor, grow_value)
    print(more)
    context = {
            'text': text,
            'fin': fin,
            'pacientes': pacientes,
            'd_none_back': ('d-none' if fin == grow_value else ''),
            'd_none_next': ('d-none' if not more else ''),
    }

    return render(request, 'crudromero/ver_todo.html', context)

def modificar(request, id):
    paciente = Paciente.objects.get(id=id)
    if request.method == 'POST':
        form = PacienteForm(request.POST, instance=paciente)
        if form.is_valid():
            form.save()
            return redirect('inicio')
        else:
            print(form.errors)
    
    context = {'paciente': paciente, 'button': 'Modificar'}
    return render(request, 'crudromero/registro.html', context)

@api_view(['GET'])
def get_data(request):
    # Return all data startswith request.GET['text']
    text = request.GET['text'].split('-')
    pacientes, _, _ = get_query_result(text, False)
    serializer = PacienteSerializer(pacientes, many=True)
    print(serializer.data)

    return Response(serializer.data)
