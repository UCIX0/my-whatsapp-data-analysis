import pandas as pd
from datetime import timedelta

def analizar_inicios(df, umbral_minutos=60):
    df = df.sort_values(by='datetime').reset_index(drop=True)
    df['time_diff'] = df['datetime'].diff().fillna(pd.Timedelta(seconds=0))

    # Nueva columna que indica si ese mensaje es un nuevo inicio de conversación
    df['new_convo'] = df['time_diff'] > timedelta(minutes=umbral_minutos)

    # Filtramos solo los mensajes que inician conversación
    inicios = df[df['new_convo']]

    # Contamos quién inicia más
    conteo = inicios['user'].value_counts()
    total = conteo.sum()
    proporciones = conteo / total
    countprop = pd.DataFrame({
        'user': conteo.index,
        'Inicia': conteo.values,
        '% Inicios': proporciones.values
    })
    return countprop.reset_index(drop=True), inicios