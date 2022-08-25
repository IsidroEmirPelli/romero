import pandas as pd


def get_all_internaciones(df):
    """Esta funcion devuelve el total de pacientes con internacion voluntaria, involuntaria y No."""
    data = dict(df['internacion'].value_counts())
    involuntario = int(data.get('Involuntaria', 0))
    voluntario = int(data.get('Voluntaria', 0))
    no = int(data.get('No', 0))

    return involuntario, voluntario, no


def torta_internados(involuntario, voluntario):
    """Esta funcion recibe el total de pacientes involuntarios y voluntarios y
    genera una torta con el total de pacientes internados."""
    labels = ['Involuntaria', 'Voluntaria']
    sizes = [involuntario, voluntario]

    return {'data': sizes, 'labels': labels}


def torta_pacientes_total_internados(total, total_internados):
    """Esta funcion recibe el total de pacientes y el total de pacientes internados y genera un grafico de torta."""
    labels = ['Total pacientes', 'Total internados']
    sizes = [total, total_internados]

    return {'data': sizes, 'labels': labels}


def get_data_torta(df, key):
    data = df[key].value_counts()
    labels = list(data.keys())
    data = data.values.tolist()

    return {'data': data, 'labels': labels}


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

    return {'data': list(map(lambda x: int(x), sizes)), 'labels': labels}
