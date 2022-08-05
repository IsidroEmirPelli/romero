import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.style as mplstyle
from sqlite3 import connect


def data_visualization():
    """
    Esta funcion genera todas las imagenes de los graficos.
    """
    conn = connect('db.sqlite3')
    df = pd.read_sql_query("SELECT * FROM crudromero_paciente", conn)
    df_visitas = pd.read_sql_query('SELECT * FROM crudromero_visita', conn)
    conn.close()

    # Checkeo si la base de datos no está vacía.
    if len(df != 0):

        involuntario, voluntario, no = get_all_internaciones(df)

        total = involuntario + voluntario + no
        torta_por_barrio(df)
        torta_internados(involuntario, voluntario)
        get_days_data(df, df_visitas)
        torta_pacientes_total_internados(no, involuntario + voluntario)
        torta_pacientes_por_derivacion(df)
        torta_por_region_sanitaria(df)

        return total
    else:
        return None


def get_all_internaciones(df):
    """Esta funcion devuelve el total de pacientes con internacion voluntaria, involuntaria y No."""
    data = df['internacion'].value_counts()
    involuntario = dict(data).get('Involuntaria') or 0
    voluntario = dict(data).get('Voluntaria') or 0
    no = dict(data).get('No') or 0

    return involuntario, voluntario, no


def torta_internados(involuntario, voluntario):
    """Esta funcion recibe el total de pacientes involuntarios y voluntarios y
    genera una torta con el total de pacientes internados."""
    labels = 'Involuntaria', 'Voluntaria'
    sizes = [involuntario, voluntario]
    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media', 'internados.png'))
    plt.clf()


def torta_pacientes_total_internados(total, total_internados):
    """Esta funcion recibe el total de pacientes y el total de pacientes internados y genera un grafico de torta."""
    labels = 'Total pacientes', 'Total internados'
    sizes = [total, total_internados]
    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    ax1.axis('equal')

    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media',  'total_pacientes.png'))
    plt.clf()


def torta_pacientes_por_derivacion(df):
    """Esta funcion genera un grafico de torta con el total de pacientes dependiendo de su derivacion."""
    data = df['derivacion'].value_counts()
    ext = data.get('Consultorios externos del hospital') or 0
    xi = data.get('Región sanitaria XI') or 0
    vi = data.get('Region Sanitaria VI') or 0
    otras = data.get('Otras') or 0
    labels = 'Consultorios externos\ndel hospital', 'Región sanitaria XI', 'Region Sanitaria VI', 'Otras'
    sizes = [ext, xi, vi, otras]
    explode = (0.1, 0, 0, 0)
    _, ax1, = plt.subplots()
    ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    ax1.axis('equal')

    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media', 'pacientes_derivacion.png'))
    plt.clf()


def torta_por_region_sanitaria(df):
    """Esta funcion genera un grafico de torta con el total de pacientes dependiendo de su region sanitaria."""
    data = df['region_sanitaria'].value_counts()
    labels = list(data.keys())
    sizes = data
    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax1.axis('equal')

    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media', 'region_sanitaria.png'))
    plt.clf()


def torta_por_barrio(df):
    """Esta funcion genera un grafico de torta con el total de pacientes dependiendo de su barrio."""
    data = df['barrio'].value_counts()
    labels = list(data.keys())
    sizes = data

    _, ax1 = plt.subplots()
    ax1.pie(sizes, labels=labels, autopct='%1.1f%%',
            shadow=True, startangle=90)

    ax1.axis('equal')
    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media', 'barrios.png'))
    plt.clf()


def get_days_data(df, df_visitas):
    """Esta funcion genera un grafico de barras con el total de pacientes internados por dia."""
    dias = {'Monday': 'Lunes', 'Tuesday': 'Martes',
            'Wednesday': 'Miércoles', 'Thursday': 'Jueves',
            'Friday': 'Viernes', 'Saturday': 'Sábado', 'Sunday': 'Domingo'}

    df['fecha'] = pd.to_datetime(df['fecha'])
    df['day_of_week'] = df['fecha'].dt.day_name()
    df['day_of_week'] = df['day_of_week'].replace(dias)

    df_visitas['day_of_week'] = pd.to_datetime(
        df_visitas['fecha']).dt.day_name().replace(dias)

    df_todo = pd.concat([df['day_of_week'], df_visitas['day_of_week']])

    data = df_todo.value_counts()
    labels = [dias[k] for k in dias]
    sizes = [data[v] if v in data else 0 for k, v in dias.items()]
    plt.bar(labels, sizes)
    plt.ylabel('Cantidad de pacientes')
    plt.title('Cantidad de pacientes por dia')
    plt.savefig(os.path.join(os.getcwd(), 'crudromero',
                'static', 'media', 'dias.png'))
    plt.clf()
