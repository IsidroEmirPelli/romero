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

def get_query_result(text, all=False, fin=0):

    limit = 5 if not all else fin

    if text[1] == 'undefined':
        if text[0].isdigit():
            pacientes = Paciente.objects.filter(dni__startswith=text[0])[:limit]
        else:
            pacientes = Paciente.objects.filter(nombre__startswith=text[0])[:limit]
    else:
        if text[0].isdigit():
            pacientes = Paciente.objects.filter(dni__startswith=text[0], nombre__startswith=text[1])[:limit]
        else:
            pacientes = Paciente.objects.filter(dni__startswith=text[1], nombre__startswith=text[0])[:limit]

    return pacientes

def ver_todo(request, text, fin):

    context = {
            'texto': text,
            'fin': fin,
            'pacientes': get_query_result(text.split('-'), True, fin),
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
    pacientes = get_query_result(text, False)
    serializer = PacienteSerializer(pacientes, many=True)
    print(serializer.data)
    return Response(serializer.data)